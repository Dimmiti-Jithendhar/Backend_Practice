from flask_restx import Namespace


class OtpDto:
    sendOtp_api=Namespace('send-otp',description='api for sending otp')
    verifyOtp_api=Namespace('verify-otp',description='api for verifying otp')
    resetPassword_api=Namespace('reset-password',description='api for reset password')
