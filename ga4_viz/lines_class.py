from .color_class import Color

class Lines:
    """
    Gestion des palettes de couleur pour les graphiques.
    Fournit une palette de 20 couleurs au format RGBA.
    """
    # -------------
    # Constructor
    # -------------
    def __init__(self, 
           account_id, model, fct, table, dimension, metric, filter, mapping):
        """
        :param self: Description
        :param account_id: Description
        :param model: Description
        :param dimension: Description
        :param metric: Description
        n:param filter: 'date_min' or 'metric-min'
        """
        self.account_id = account_id
        self.model = model
        self.sum_or_average = fct # SUM, AVG
        self.table = table
        self.dimension = dimension # deviceCategory, TrafficSource, ...
        self.metric = metric # active Users, sessions
        self.filter = filter
        self.color = Color() # load palette
        
        # cached datas
        self.months = None
        self.dimensions = None
        self.datasets = None
        self.debug = None

        # read mapping 
        # {'facebook': 'l.facebook.com', 'm.facebook.com'} -> {'facebook': "'l.facebook.com'", "'m.facebook.com'"}
        self.mapping = None
        if mapping is not None:
            self.mapping = {}  
            for k, values in mapping.items():
                if k not in self.mapping:
                    self.mapping[k] = []
                for v in values:    
                    self.mapping[k].append(f"'{v}'")
                

    def get_sql_filter(self):
        where = []
        where.append(f"account_id = {self.account_id}")
        if 'date_min' in self.filter and self.filter['date_min'] is not None:
            where.append(f"date>='{ self.filter['date_min'] }'")
        if 'metric_min' in self.filter and self.filter['metric_min'] is not None:
            where.append(f"{self.metric}>={ self.filter['metric_min']}" )
        return f"WHERE {' AND '.join(where)}"


    def get_sql_mapping(self):
        if self.mapping is None:
            return self.dimension

        mapping_rules = []
        for k, values  in self.mapping.items():
             mapping_rules.append(f"WHEN {self.dimension} IN ({','.join(values)}) THEN '{k}'")

        return f"""
            CASE 
               {'\n'.join(mapping_rules)}
                ELSE {self.dimension}
            END    
            """
        

    # -------------
    # Dimensions
    # -------------
    def get_dimensions(self) -> dict:
        """
        Format dictionary: {dimension: SUM(metric)}
        """
        if self.dimensions is not None:
            return self.dimensions
            
        dimension_values = {}
        sql = f"""
            SELECT 
                MIN(id) AS id, 
                {self.get_sql_mapping()} AS dimension,
                {self.sum_or_average}({self.metric}) AS metric_value
            FROM {self.table}
            {self.get_sql_filter()} 
            GROUP BY {self.get_sql_mapping()}
            ORDER BY metric_value DESC
        """
        self.debug = sql
        rows = self.model.objects.raw(sql)
        for row in rows:
            dimension_values[ row.dimension ] = int(row.metric_value)
            
        self.dimensions = dimension_values
        return self.dimensions


    # -------------
    # Months
    # -------------
    def get_months(self):
        """
        All months
        """
        if self.months is not None:
            return self.months
        
        rows = self.model.objects.raw(f"""
            SELECT 
                MIN(id) AS id, 
                LEFT(date,7) AS month
            FROM {self.table}
            {self.get_sql_filter()} 
            GROUP BY LEFT(date,7)
            ORDER BY LEFT(date,7) ASC
        """)
        months = []
        for row in rows:
            months.append(row.month)
        self.months = months
        return self.months


    # ------------------
    # Chart FX datasets
    # ------------------
    def get_datasets(self):
        if self.datasets is not None:
            return self.datasets

        # Full initialisation with blank values        
        metrics = {}
        for dimension in self.get_dimensions():  # all dimensions
            metrics[dimension] = {}
            for month in self.get_months(): # all months
                metrics[dimension][month] = 0

        # Fill metrics
        sql = f"""
            SELECT 
                MIN(id) AS id, 
                LEFT(date,7) AS month,
                {self.get_sql_mapping()} AS dimension,
                {self.sum_or_average}({self.metric}) AS metric_value        
            FROM {self.table}
            {self.get_sql_filter()}                         
        GROUP BY LEFT(date,7), {self.get_sql_mapping()}
        ORDER BY LEFT(date,7) ASC
        """
        print(sql)
        rows = self.model.objects.raw(sql)
        for row in rows:
            metrics[ row.dimension ][row.month] = int(row.metric_value)
        
        # Fill datasets with all metrics 
        datasets = []
        i = -1
        for dimension in self.get_dimensions():
            i += 1
            datasets.append({
                'label': dimension,
                'datas': list(metrics[ dimension ].values()),
                'borderColor': self.color.get_rgba_foreground(i),
                'backgroundColor': self.color.get_rgba_background(i),
                'fill': 'true',
                'borderWidth': 2,
                'stack': 'stack1'
            })
        self.datasets = datasets
        return self.datasets
