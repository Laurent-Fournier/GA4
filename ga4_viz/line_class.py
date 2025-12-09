from typing import Dict, List, Optional, Any
from .color_class import Color

class Line:
    """Represents a line in a chart, with data fetched from a database table."""
    
    
    def __init__(self, 
        account_id: int, 
        model: Any, 
        agregation_function: str,  # 'SUM' or 'AVG'
        table: str, 
        metric: str,
        filter: Dict[str, Any],
        color_index: int
        ):
        """
        Args:        
            account_id: ID of the account to filter data.
            model: Django model class for database queries.
            fct: Aggregation function ('SUM' or 'AVG').
            table: Name of the database table.
            metric: Name of the metric column.
            filter: Dictionary of filters (e.g., {'date_min': '2023-01-01', 'metric_min': 100}).
        """
        self.account_id = account_id
        self.model = model
        self.sum_or_average = agregation_function.upper() # SUM, AVG        
        self.table = table
        self.metric = metric # active Users, sessions
        self.filter = filter
        self.color = Color()
        self.color_index = color_index
        
        # cached data
        self._months = None
        self._datasets = None

    def _build_sql_where(self) -> str:
        """Builds the WHERE clause for SQL queries."""        
        where = [f"account_id = {self.account_id}"]
        if 'date_min' in self.filter and self.filter['date_min'] is not None:
            where.append(f"date>='{ self.filter['date_min'] }'")
        if 'metric_min' in self.filter and self.filter['metric_min'] is not None:
            where.append(f"{self.metric}>={ self.filter['metric_min']}" )
        return f"WHERE {' AND '.join(where)}"


    # -------------
    # Months
    # -------------
    def get_months(self) -> List[str]:
        """Returns all months for which data exists."""
        if self._months is not None:
            return self._months
        
        rows = self.model.objects.raw(f"""
            SELECT 
                MIN(id) AS id, 
                LEFT(date,7) AS month
            FROM {self.table}
            {self._build_sql_where()} 
            GROUP BY LEFT(date,7)
            ORDER BY LEFT(date,7) ASC
        """)
        months = []
        for row in rows:
            months.append(row.month)
        self._months = months
        return self._months


    # ------------------
    # Chart FX datasets
    # ------------------
    def get_datasets(self):
        """Returns datasets for Chart.js."""        
        if self._datasets is not None:
            return self.datasets

        # Full initialisation with blank values        
        metrics = {}
        for month in self.get_months(): # all months
            metrics[month] = 0

        # Fill metrics
        sql = f"""
            SELECT 
                MIN(id) AS id, 
                LEFT(date,7) AS month,
                {self.sum_or_average}({self.metric}) AS metric_value        
            FROM {self.table}
            {self._build_sql_where()}                         
        GROUP BY LEFT(date,7)
        ORDER BY LEFT(date,7) ASC
        """
        print(sql)
        rows = self.model.objects.raw(sql)
        for row in rows:
            metrics[row.month] = int(row.metric_value) if self.sum_or_average == 'SUM' else float(row.metric_value)
        
        # Fill datasets with all metrics 
        datasets = [{
            'label': self.metric,
            'datas': list(metrics.values()),
            'borderColor': self.color.get_rgba_foreground(self.color_index),
            'backgroundColor': self.color.get_rgba_background(self.color_index),
            'fill': 'true',
            'borderWidth': 2,
            'stack': 'stack1'
        }]
        self._datasets = datasets
        return self._datasets
