class Line:
    """
    Gestion des palettes de couleur pour les graphiques.
    Fournit une palette de 20 couleurs au format RGBA.
    """

    # -------------
    # Constructor
    # -------------
    def __init__(self, account_id, model, table, dimension, metric, filter):
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
        self.table = table
        self.dimension = dimension
        self.metric = metric
        self.filter = filter

    def get_dimension_values(self) -> dict:
        """
        Format dictionary: {dimension: SUM(metric)}
        """
        where = []
        where.append(f"account_id = {self.account_id}")
        if 'date_min' in self.filter and self.filter['date_min'] is not None:
            where.append(f"date>='{ self.filter['date_min'] }'")
        if 'metric_min' in self.filter and self.filter['metric_min'] is not None:
            where.append(f"metric>={ self.filter['metric_min']}" )
        sql_where = f"WHERE {' AND '.join(where)}"
                
        dimension_values = {}
        rows = self.model.objects.raw(f"""
            SELECT 
                MIN(id) AS id, 
                {self.dimension} AS dimension, 
                SUM({self.metric}) AS metric_value
            FROM {self.table}
            {sql_where} 
            GROUP BY {self.dimension}
            ORDER BY metric_value DESC
        """)
        for row in rows:
            dimension_values[ row.dimension ] = int(row.metric_value)
            
        return dimension_values



		# "dimensions": ["date", "sessionDefaultChannelGrouping"],
		# "metrics": ["sessions"],
  
  		# "dimensions": ["date", "deviceCategory"],
		# "metrics": ["activeUsers"],