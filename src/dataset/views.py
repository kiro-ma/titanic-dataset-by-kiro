from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import DataSetSerializer
from .models import DataSet
import pandas as pd
import numpy as np


class DatasetViewSet(ModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Retorna um resumo estatístico das colunas numéricas."""
        
        data = pd.DataFrame.from_records(DataSet.objects.values())

        if data.empty:
            return Response({"error": "No data available"}, status=status.HTTP_400_BAD_REQUEST)

        numeric_columns = ["age", "fare", "parch"]
        numeric_data = data[numeric_columns].apply(pd.to_numeric)

        numeric_data = numeric_data.astype(float)

        # Calcula as estatísticas básicas

        # count: Número total de elementos não nulos na coluna.
        # mean: Média aritmética dos valores da coluna.
        # std: Desvio padrão, que mede a dispersão dos dados em relação à média.
        # min: Valor mínimo presente na coluna.
        # max: Valor máximo presente na coluna.
        # median: Valor central da coluna quando os dados estão ordenados

        summary_stats = numeric_data.agg(
            ["count", "mean", "std", "min", "max", "median"]
        ).round(2)

        result = summary_stats.to_dict()

        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def survival_rate(self, request):
        """Retorna a taxa de sobrevivência global."""
        data = DataSet.objects.values_list("survived", flat=True)
        survived = np.array(data)

        if len(survived) == 0:
            return Response({"error": "No data available"}, status=status.HTTP_400_BAD_REQUEST)

        survival_rate = (np.mean(survived) * 100).round(2)

        return Response({"survival_rate": survival_rate}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def survival_rate_by_group(self, request):
        """Retorna a taxa de sobrevivência agrupada por uma coluna específica."""
        group_by = request.query_params.get("group_by", None)

        if not group_by:
            return Response(
                {"error": "You must provide a 'group_by' parameter (e.g., Sex, Pclass, Embarked)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not hasattr(DataSet, group_by):
            return Response(
                {"error": f"Invalid column name: {group_by}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = pd.DataFrame.from_records(DataSet.objects.values(group_by, "survived"))

        if data.empty:
            return Response({"error": "No data available"}, status=status.HTTP_400_BAD_REQUEST)

        grouped = data.groupby(group_by)["survived"].mean().mul(100).round(2)

        result = grouped.reset_index().to_dict(orient="records")

        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def correlation(self, request):
        """Retorna a matriz de correlação entre as variáveis numéricas."""
        numeric_data = pd.DataFrame.from_records(DataSet.objects.values(
            "age", "fare", "sib_sp", "parch", "survived"
        ))

        # Remove valores nulos para evitar erros ao calcular a correlação
        numeric_data = numeric_data.dropna()

        if numeric_data.empty:
            return Response({"error": "No numeric data available"}, status=status.HTTP_400_BAD_REQUEST)

        # Calcula a matriz de correlação
        correlation_matrix = numeric_data.corr()

        result = correlation_matrix.to_dict()

        return Response(result, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def clean_data(self, request):
        """Recebe um conjunto de dados e realiza limpeza nas colunas 'Age', 'Fare' e 'Embarked'."""
        try:
            data = request.data

            df = pd.DataFrame(data)

            # Faz a limpeza da coluna 'Age'
            if 'age' in df.columns:
                # Remove valores negativos de 'age'
                df['age'] = df['age'].apply(lambda x: None if x < 0 else x)
                # Preenche valores ausentes com a mediana de 'age'
                median_age = df['age'].median()
                df['age'] = df['age'].fillna(median_age)

            # Faz a limpeza da coluna 'Embarked'
            if 'embarked' in df.columns:
                # Preenche valores ausentes com a moda de 'embarked' (valor mais comum)
                mode_embarked = df['embarked'].mode()[0] if not df['embarked'].mode().empty else None
                df['embarked'] = df['embarked'].fillna(mode_embarked)

            # Faz a limpeza da coluna 'Fare' (ajustar valores fora do intervalo válido)
            if 'fare' in df.columns:
                fare_lower_limit = 0
                fare_upper_limit = 500

                df['fare'] = df['fare'].apply(
                    lambda x: fare_lower_limit 
                        if x < fare_lower_limit
                        else (fare_upper_limit if x > fare_upper_limit else x)
                )

            # Substitui NaN por None
            df = df.where(pd.notna(df), None)

            cleaned_data = df.to_dict(orient='records')

            cleaned_data = [
                {k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in record.items()}
                for record in cleaned_data
            ]

            return Response(cleaned_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)









