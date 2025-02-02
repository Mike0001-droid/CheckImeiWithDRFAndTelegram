import httpx
from decouple import config

IMEICHECK_API_KEY=config('IMEICHECK_API_KEY')
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

async def check_imei(imei: str):
    headers = {
        'Authorization': f'Bearer {IMEICHECK_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'deviceId': imei,  
        'serviceId': config('SERVICE_ID'),
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.imeicheck.net/v1/checks", 
                json=data, 
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP Error: {e.response.status_code} - {e.response.text}"}
    
    except httpx.RequestError as e:
        return {"error": f"Request Error: {str(e)}"}
    
    except Exception as e:
        return {"error": f"Unexpected Error: {str(e)}"}