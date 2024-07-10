from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
import streamlit as st

examples_fewshot = [
    {
        "input": "How many t-shirts do we have left for Nike in XS size and white color?",
        "query": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Nike' AND color = 'White' AND size = 'XS';"
    },
    {
        "input": "How much is the total price of the inventory for all S-size t-shirts?",
        "query": "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S';"
    },
    {
        "input": "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?",
        "query": """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
                    (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
                    group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id;"""
    },
    {
        "input": "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?",
        "query": "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi';"
    },
    {
        "input": "How many white color Levi's shirt I have?",
        "query": "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White';"
    },
    {
     'input':"how much sales amount will be generated if we sell all large size t shirts today in nike brand after discounts?",
     "query": """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
                (select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Nike' and size="L"
                group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id;"""   
    }
]

@st.cache_resource
def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples_fewshot,
        OpenAIEmbeddings(),
        Chroma,
        k=2,
        input_keys=["input"],
    )
    return example_selector