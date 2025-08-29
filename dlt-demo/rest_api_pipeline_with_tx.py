import dlt
from dlt.sources.rest_api import rest_api_source 

def lowercase_email(record):
    record['email'] = record['email'].lower()
    return record

restapi_source = rest_api_source({
    'client':{
        'base_url':"https://jsonplaceholder.typicode.com/"
    },
    'resources': [
        {
            'name': 'users',
            'processing_steps':[
                {"filter":lambda x: x['id']%2 != 0} # let say we only want odd user IDs
                ,{"map":lowercase_email} # custom processing step to lowercase email
            ]
        }, 
        'posts', 
        'comments']
})


pipeline = dlt.pipeline(
    pipeline_name="rest_api_minimal",
    destination='duckdb',
    dataset_name="rest_api_data",
)

if __name__ == "__main__":
    pipeline.run(restapi_source)

    with pipeline.sql_client() as conn:
        # Manual primary key constraint creation
        conn.execute("ALTER TABLE rest_api_data.users ADD CONSTRAINT users_pk PRIMARY KEY (id)") # need to delete existing *.duckdb if exist
        