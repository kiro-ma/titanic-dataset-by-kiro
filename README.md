# Titanic Data Analysis - By Kiro Marcell

Este é um projeto django focado em análise de dados com a base de dados Titanic. A aplicação expõe uma API RESTful para processar e analisar os dados do Titanic, com funcionalidades que incluem análise estatística, taxa de sobrevivência, correlação entre variáveis e limpeza de dados.

## Endpoints

### 1. **GET /api/summary**

Retorna um resumo estatístico das colunas numéricas, como `age`, `fare`, `sib_sp`, `parch`, e outras métricas básicas.

#### Resposta:
```json
{
  "age": {
    "count": 714,
    "mean": 29.70,
    "std": 14.53,
    "min": 0.42,
    "max": 80.00,
    "median": 28.00
  },
  "fare": {
    "count": 714,
    "mean": 33.29,
    "std": 51.76,
    "min": 0.00,
    "max": 512.33,
    "median": 14.45
  },
  "sib_sp": {
    "count": 714,
    "mean": 0.52,
    "std": 1.03,
    "min": 0,
    "max": 8
  },
  "parch": {
    "count": 714,
    "mean": 0.38,
    "std": 0.81,
    "min": 0,
    "max": 6
  }
}
```

### 2. **GET /api/survival_rate**

Retorna a taxa global de sobrevivência dos passageiros.

#### Resposta:
```json
{
  "survival_rate": 38.38
}
```

### 3. **GET /api/survival_rate_by_group?group_by=<coluna>**

Retorna a taxa de sobrevivência agrupada por uma coluna especificada. A coluna pode ser uma das seguintes: `sex`, `passenger_class`, `embarked`, etc.

#### Exemplo de requisição:

`GET /api/survival_rate_by_group?group_by=sex`

#### Resposta:
```json
[
  {"sex": "male", "survival_rate": 18.69},
  {"sex": "female", "survival_rate": 74.20}
]
```

### 4. **GET /api/correlation**

Retorna a matriz de correlação entre as variáveis numéricas da base de dados, como `age`, `fare`, `sib_sp`, `parch`, `survived`.

#### Resposta:
```json
{
  "age": {
    "age": 1.0,
    "fare": -0.03273670500134324,
    "sib_sp": -0.13878900802106603,
    "parch": -0.06648541574422728,
    "survived": -0.10692399041519621
  },
  "fare": {
    "age": -0.03273670500134324,
    "fare": 1.0,
    "sib_sp": 0.13833378286379902,
    "parch": 0.20512261555843314,
    "survived": 0.26818570088021126
  },
  "sib_sp": {
    "age": -0.13878900802106603,
    "fare": 0.13833378286379902,
    "sib_sp": 1.0,
    "parch": 0.3838198640428336,
    "survived": -0.01735836047953419
  },
  "parch": {
    "age": -0.06648541574422728,
    "fare": 0.20512261555843314,
    "sib_sp": 0.3838198640428336,
    "parch": 1.0,
    "survived": 0.09331700774224314
  },
  "survived": {
    "age": -0.10692399041519621,
    "fare": 0.26818570088021126,
    "sib_sp": -0.01735836047953419,
    "parch": 0.09331700774224314,
    "survived": 1.0
  }
}
```

### 5. **POST /api/clean_data**

Recebe um conjunto de dados no formato JSON e realiza limpeza nas colunas `age`, `fare`, e `embarked`, tratando valores ausentes, valores anômalos e valores inválidos.

#### Exemplo de requisição:
```json
[
	{
		"passengerId": 1,
		"survived": 1,
		"passengerClass": 3,
		"name": "Braund, Mr. Owen Harris",
		"sex": "male",
		"age": null, // valor inválido.
		"sib_sp": 1,
		"parch": 0,
		"ticket": "A/5 21171",
		"fare": 600, // valor inválido.
		"cabin": "C85",
		"embarked": null // valor inválido.
	},
	{
		"passengerId": 2,
		"survived": 1,
		"passengerClass": 1,
		"name": "Cumings, Mrs. John Bradley (Florence Briggs Thayer)",
		"sex": "female",
		"age": 29.5,
		"parch": 0,
		"ticket": "PC 17599",
		"fare": 71.2833,
		"cabin": "C85",
		"embarked": "C"
	}
]
```

#### Resposta:
```json
[
	{
		"passengerId": 1,
		"survived": 1,
		"passengerClass": 3,
		"name": "Braund, Mr. Owen Harris",
		"sex": "male",
		"age": 29.5, // mediana.
		"sib_sp": 1.0,
		"parch": 0,
		"ticket": "A/5 21171",
		"fare": 500.0, // valor máximo.
		"cabin": "C85",
		"embarked": "C" // valor mais comum.
	},
	{
		"passengerId": 2,
		"survived": 1,
		"passengerClass": 1,
		"name": "Cumings, Mrs. John Bradley (Florence Briggs Thayer)",
		"sex": "female",
		"age": 29.5,
		"sib_sp": null,
		"parch": 0,
		"ticket": "PC 17599",
		"fare": 71.2833,
		"cabin": "C85",
		"embarked": "C"
	}
]
```

## Requisitos
```
asgiref==3.8.1
Django==5.1.3
django-cors-headers==4.6.0
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
et_xmlfile==2.0.0
openpyxl==3.1.5
psycopg2-binary==2.9.10
PyJWT==2.9.0
python-dotenv==1.0.1
sqlparse==0.5.2
```

## Como rodar o projeto

#### 1. Clone o repositório:
```
git clone https://github.com/kiro-ma/titanic-dataset-by-kiro.git
```

#### 2. Crie um ambiente virtual e ative-o:
```
python3 -m venv venv
source venv/bin/activate  # no Linux ou Mac
venv\Scripts\activate  # no Windows
```

#### 3. Instale as dependências:
```
pip install -r requirements.txt
```

#### 4. Realize as migrações do banco de dados:
```
python manage.py migrate
```

#### 6. Acesse a API em `http://127.0.0.1:8000/api/`


