import azure.functions as func
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('{{ function_name }} function processed a request.')

    try:
        # Add your function logic here
        return func.HttpResponse(
            "Function executed successfully!",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error in {{ function_name }}: {str(e)}")
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
