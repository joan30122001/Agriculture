# from django.conf import settings
# from django.core.signals import request_finished



# class PayStack:
#     PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
#     base_url = 'https://api.paystack.co'

#     def cerify_payment(self, ref, *args, **kwargs):
#         path = f'/transaction/verify/{ref}'

#         headers = {
#             "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
#             'Content_Type': 'application/json',
#         }
#         url = self.base_url + path
#         response = requests.get(url, headers=headers)

#         if response.status_code = 200:
#             response_data = response.json()
#             return response_data['status'], response_data['data']
#         response.data = response.json()
#         return response_data["status"], response_data["message"]