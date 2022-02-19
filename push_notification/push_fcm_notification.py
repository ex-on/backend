from firebase_admin import messaging


def send_to_firebase_cloud_messaging():
    # This registration token comes from the client FCM SDKs.
    # registration_token = 'fWpT3We5Q12Ex1wYczzgq6:APA91bHzELZeZmsACcXiULvKmdjfQm7uMgJouxD-HcN1_Rbg28oM5lYRMKqL_Z8l_asXZ2ujEhXQSMkKAgOyak07yhNWCgPwuP86DCOqTl5K1thwT2KnH9eR5_IIvAiMjTdlTvmw8Hb0'
    # registration_token = 'ewDSmOi0TcmqqRUFU8Wbvc:APA91bFX4wp-uEwSLi7YhTI1YrZpsf6bLVJ05ytKNyq7_g8PXwV6mbgMdcnKiAc35ElvF4XlZSHjx74bEBjS7GIi9H-F8vV1K6cE18fioGWHPLI67qwbn79Ha4cpP8Yb0C03Pu_hZGVV'

    # See documentation on defining a message payload.
    # message = messaging.Message(
    #     notification=messaging.Notification(
    #         title='환영합니다!🤗',
    #         body='엑손의 회원가입을 축하드려요!🎉',
    #     ),
    #     token=registration_token,
    # )

    # response = messaging.send(message)
    # Response is a message ID string.
    # print('Successfully sent message:', response)
    print('yo')
