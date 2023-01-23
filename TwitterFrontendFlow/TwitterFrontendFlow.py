import requests
import json
import pysnooper

#追加
# 加工した画像ファイルをbase64変換する-
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont


def pil_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="jpeg")
    img_str = base64.b64encode(buffer.getvalue()).decode("ascii")
    return img_str


class TwitterFrontendFlow:
    def __init__(self, ua="", proxies={}, language="en"):
        if not ua:
            # self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        else:
            self.USER_AGENT = ua
        self.AUTHORIZATION = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self.proxies = proxies
        self.session = requests.session()
        self.__twitter()
        self.x_guest_token = self.__get_guest_token()
        self.method_check_bypass = False
        self.flow_token = None
        self.language = language

    def __twitter(self):
        headers = {
            "User-Agent": self.USER_AGENT,
        }
        response = self.session.get(
            "https://twitter.com/", headers=headers, proxies=self.proxies
        )
        return self

    def __get_guest_token(self):
        headers = {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
        }
        response = self.session.post(
            "https://api.twitter.com/1.1/guest/activate.json",
            headers=headers,
            proxies=self.proxies,
        ).json()
        return response["guest_token"]

    def __get_headers(self):
        return {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
            "Content-type": "application/json",
            "x-guest-token": self.x_guest_token,
            "x-csrf-token": self.session.cookies.get("ct0"),
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": self.language,
        }

    #追加
    def __get_change_country_headers(self):
        return {
            "authorization": self.AUTHORIZATION,
            "referer": "https://twitter.com/i/flow/settings/change_country?return_path=%2Fsettings%2Fcountry",
            "User-Agent": self.USER_AGENT,
            "Content-type": "application/json",
            "x-guest-token": self.x_guest_token,
            "x-csrf-token": self.session.cookies.get("ct0"),
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": self.language,
        }

    def __get_headers_legacy(self):
        return {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
            "Content-type": "application/x-www-form-urlencoded",
            "x-csrf-token": self.session.cookies.get("ct0"),
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
        }

    def get_subtask_ids(self):
        return [subtasks["subtask_id"] for subtasks in self.content["subtasks"]]

    def __flow_token_check(self):
        if self.flow_token == None:
            raise Exception("not found token")

    def __error_check(self):
        if self.content.get("errors"):
            raise Exception(self.content["errors"][0]["message"])

    def __method_check(self, method_name):
        if self.method_check_bypass:
            return
        if method_name not in self.get_subtask_ids():
            raise Exception(
                "{0} is inappropriate method. choose from {1}. information: https://github.com/fa0311/TwitterFrontendFlow#inappropriate-method".format(
                    method_name, ", ".join(self.get_subtask_ids())
                )
            )

    def LoadCookies(self, file_path):
        with open(file_path, "r") as f:
            for cookie in json.load(f):
                self.session.cookies.set_cookie(
                    requests.cookies.create_cookie(**cookie)
                )
        return self

    def SaveCookies(self, file_path):
        cookies = []
        for cookie in self.session.cookies:
            cookie_dict = dict(
                version=cookie.version,
                name=cookie.name,
                value=cookie.value,
                port=cookie.port,
                domain=cookie.domain,
                path=cookie.path,
                secure=cookie.secure,
                expires=cookie.expires,
                discard=cookie.discard,
                comment=cookie.comment,
                comment_url=cookie.comment_url,
                rfc2109=cookie.rfc2109,
                rest=cookie._rest,
            )
            cookies.append(cookie_dict)

        with open(file_path, "w") as f:
            json.dump(cookies, f, indent=4)
        return self


    #追加

    def change_country_flow(self, country_code="jp"):
        

        params = {
            "flow_name": "settings/change_country",
        }

        json_data = {
            "input_flow_data": {
                "country_code": country_code,
                "flow_context": {
                    "debug_overrides": {},
                    "start_location": {
                        "location": "settings",
                    },
                },
            },
            "subtask_versions": {
                "action_list": 2,
                "alert_dialog": 1,
                "app_download_cta": 1,
                "check_logged_in_account": 1,
                "choice_selection": 3,
                "contacts_live_sync_permission_prompt": 0,
                "cta": 7,
                "email_verification": 2,
                "end_flow": 1,
                "enter_date": 1,
                "enter_email": 2,
                "enter_password": 5,
                "enter_phone": 2,
                "enter_recaptcha": 1,
                "enter_text": 5,
                "enter_username": 2,
                "generic_urt": 3,
                "in_app_notification": 1,
                "interest_picker": 3,
                "js_instrumentation": 1,
                "menu_dialog": 1,
                "notifications_permission_prompt": 2,
                "open_account": 2,
                "open_home_timeline": 1,
                "open_link": 1,
                "phone_verification": 4,
                "privacy_options": 1,
                "security_key": 3,
                "select_avatar": 4,
                "select_banner": 2,
                "settings_list": 7,
                "show_code": 1,
                "sign_up": 2,
                "sign_up_review": 4,
                "tweet_selection_urt": 1,
                "update_users": 1,
                "upload_media": 1,
                "user_recommendations_list": 4,
                "user_recommendations_urt": 1,
                "wait_spinner": 3,
                "web_modal": 1,
            },
        }

        response = self.session.post("https://twitter.com/i/api/1.1/onboarding/task.json", params=params, headers=self.__get_change_country_headers(), json=json_data).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def change_country_subtask(self):
        
        json_data = {
            'flow_token': self.flow_token,
            'subtask_inputs': [
                {
                    'subtask_id': 'CallToAction',
                    'cta': {
                        'link': 'consent_agree_link',
                    },
                },
            ],
        }

        response = self.session.post('https://twitter.com/i/api/1.1/onboarding/task.json', headers=self.__get_change_country_headers(), json=json_data).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def change_country_end(self):
        
        json_data = {
            'flow_token': self.flow_token,
            'subtask_inputs': [],
        }

        response = requests.post('https://twitter.com/i/api/1.1/onboarding/task.json', headers=self.__get_change_country_headers(), json=json_data).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    # ログイン

    def login_flow(self):
        data = {
            "input_flow_data": {
                "flow_context": {
                    "debug_overrides": {},
                    "start_location": {"location": "splash_screen"},
                }
            },
            "subtask_versions": {
                "contacts_live_sync_permission_prompt": 0,
                "email_verification": 1,
                "topics_selector": 1,
                "wait_spinner": 1,
                "cta": 4,
            },
        }
        params = {"flow_name": "login"}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            params=params,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginJsInstrumentationSubtask(self):
        self.__flow_token_check()
        self.__method_check("LoginJsInstrumentationSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginJsInstrumentationSubtask",
                    "js_instrumentation": {
                        "response": json.dumps(
                            {
                                "rf": {
                                    "af07339bbc6d24ced887d705eb0c9fd29b4a7d7ddc21136c9f94d53a4bc774d2": 88,
                                    "a6ce87d6481c6ec4a823548be3343437888441d2a453061c54f8e2eb325856f7": 250,
                                    "a0062ad06384a8afd38a41cd83f31b0dbfdea0eff4b24c69f0dd9095b2fb56d6": 16,
                                    "a929e5913a5715d93491eaffaa139ba4977cbc826a5e2dbcdc81cae0f093db25": 186,
                                },
                                "s": "Q-H-53m1uXImK0F0ogrxRQtCWTH1KIlPbIy0MloowlMa4WNK5ZCcDoXyRs1q_cPbynK73w_wfHG_UVRKKBWRoh6UJtlPS5kMa1p8fEvTYi76hwdzBEzovieR8t86UpeSkSBFYcL8foYKSp6Nop5mQR_QHGyEeleclCPUvzS0HblBJqZZdtUo-6by4BgCyu3eQ4fY5nOF8fXC85mu6k34wo982LMK650NsoPL96DBuloqSZvSHU47wq2uA4xy24UnI2WOc6U9KTvxumtchSYNnXq1HV662B8U2-jWrzvIU4yUHV3JYUO6sbN6j8Ho9JaUNJpJSK7REwqCBQ3yG7iwMAAAAX2Vqcbs",
                            }
                        ),
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginEnterUserIdentifierSSO(self, user_id):
        self.__flow_token_check()
        self.__method_check("LoginEnterUserIdentifierSSO")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterUserIdentifierSSO",
                    "settings_list": {
                        "setting_responses": [
                            {
                                "key": "user_identifier",
                                "response_data": {"text_data": {"result": user_id}},
                            }
                        ],
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def AccountDuplicationCheck(self):
        self.__flow_token_check()
        self.__method_check("AccountDuplicationCheck")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "AccountDuplicationCheck",
                    "check_logged_in_account": {
                        "link": "AccountDuplicationCheck_false"
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginEnterAlternateIdentifierSubtask(self, text):
        self.__flow_token_check()
        self.__method_check("LoginEnterAlternateIdentifierSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterAlternateIdentifierSubtask",
                    "enter_text": {"text": text, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginEnterPassword(self, password):
        self.__flow_token_check()
        self.__method_check("LoginEnterPassword")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterPassword",
                    "enter_password": {"password": password, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginTwoFactorAuthChallenge(self, TwoFactorCode):
        self.__flow_token_check()
        self.__method_check("LoginTwoFactorAuthChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginTwoFactorAuthChallenge",
                    "enter_text": {"text": TwoFactorCode, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginAcid(self, acid):
        self.__flow_token_check()
        self.__method_check("LoginAcid")
        data = {
            "flow_token":self.flow_token,
            "subtask_inputs":[
                {
                    "subtask_id":"LoginAcid",
                    "enter_text":
                        {
                            "text": acid,
                            "link":"next_link"
                        }
                    }
                ]
            }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self


    # attの取得 無くても動くっぽい

    def get_att(self):
        data = {"flow_token": self.flow_token, "subtask_inputs": []}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    # ct0の更新 無くても動くっぽい

    def Viewer(self):
        params = {
            "variables": json.dumps(
                {
                    "withCommunitiesMemberships": True,
                    "withCommunitiesCreation": True,
                    "withSuperFollowsUserFields": True,
                }
            )
        }
        response = self.session.get(
            "https://twitter.com/i/api/graphql/O_C5Q6xAVNOmeolcXjKqYw/Viewer",
            headers=self.__get_headers(),
            params=params,
        )

        self.content = response
        self.__error_check()
        return self

    def RedirectToPasswordReset(self):
        raise Exception(
            "RedirectToPasswordResetは現在サポートされていません。代わりにpassword_reset_flowを使用して下さい。"
        )

    # パスワードリセット

    def password_reset_flow(self):
        data = {
            "input_flow_data": {
                "flow_context": {
                    "debug_overrides": {},
                    "start_location": {"location": "manual_link"},
                }
            },
            "subtask_versions": {
                "contacts_live_sync_permission_prompt": 0,
                "email_verification": 1,
                "topics_selector": 1,
                "wait_spinner": 1,
                "cta": 4,
            },
        }
        params = {"flow_name": "password_reset"}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            params=params,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PwrJsInstrumentationSubtask(self):
        self.__flow_token_check()
        self.__method_check("PwrJsInstrumentationSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PwrJsInstrumentationSubtask",
                    "js_instrumentation": {
                        "response": json.dumps(
                            {
                                "rf": {
                                    "af07339bbc6d24ced887d705eb0c9fd29b4a7d7ddc21136c9f94d53a4bc774d2": 88,
                                    "a6ce87d6481c6ec4a823548be3343437888441d2a453061c54f8e2eb325856f7": 250,
                                    "a0062ad06384a8afd38a41cd83f31b0dbfdea0eff4b24c69f0dd9095b2fb56d6": 16,
                                    "a929e5913a5715d93491eaffaa139ba4977cbc826a5e2dbcdc81cae0f093db25": 186,
                                },
                                "s": "Q-H-53m1uXImK0F0ogrxRQtCWTH1KIlPbIy0MloowlMa4WNK5ZCcDoXyRs1q_cPbynK73w_wfHG_UVRKKBWRoh6UJtlPS5kMa1p8fEvTYi76hwdzBEzovieR8t86UpeSkSBFYcL8foYKSp6Nop5mQR_QHGyEeleclCPUvzS0HblBJqZZdtUo-6by4BgCyu3eQ4fY5nOF8fXC85mu6k34wo982LMK650NsoPL96DBuloqSZvSHU47wq2uA4xy24UnI2WOc6U9KTvxumtchSYNnXq1HV662B8U2-jWrzvIU4yUHV3JYUO6sbN6j8Ho9JaUNJpJSK7REwqCBQ3yG7iwMAAAAX2Vqcbs",
                            }
                        ),
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetBegin(self, user_id):
        self.__flow_token_check()
        self.__method_check("PasswordResetBegin")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetBegin",
                    "enter_text": {"text": user_id, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetChooseChallenge(self, choices="0"):
        self.__flow_token_check()
        self.__method_check("PasswordResetChooseChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetChooseChallenge",
                    "choice_selection": {
                        "link": "next_link",
                        "selected_choices": [choices],
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PwrKnowledgeChallenge(self, text):
        self.__flow_token_check()
        self.__method_check("PwrKnowledgeChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PwrKnowledgeChallenge",
                    "enter_text": {"text": text, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetConfirmChallenge(self, code):
        self.__flow_token_check()
        self.__method_check("PasswordResetConfirmChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetConfirmChallenge",
                    "enter_text": {"text": code, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetNewPassword(self, password):
        self.__flow_token_check()
        self.__method_check("PasswordResetNewPassword")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetNewPassword",
                    "enter_password": {"password": password, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetSurvey(self, choices="0"):
        self.__flow_token_check()
        self.__method_check("PasswordResetSurvey")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetSurvey",
                    "choice_selection": {
                        "link": "next_link",
                        "selected_choices": [choices],
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    # ログイン後

    def CreateTweet(self, tweet_text):
        data = {
            "queryId": "XyvN0Wv13eeu_gVIHDi10g",
            "variables": json.dumps(
                {
                    "tweet_text": tweet_text,
                    "media": {"media_entities": [], "possibly_sensitive": False},
                    "withDownvotePerspective": False,
                    "withReactionsMetadata": False,
                    "withReactionsPerspective": False,
                    "withSuperFollowsTweetFields": True,
                    "withSuperFollowsUserFields": False,
                    "semantic_annotation_ids": [],
                    "dark_request": False,
                    "withBirdwatchPivots": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/XyvN0Wv13eeu_gVIHDi10g/CreateTweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def FavoriteTweet(self, tweet_id):
        data = {
            "queryId": "lI07N6Otwv1PhnEgXILM7A",
            "variables": json.dumps(
                {
                    "tweet_id": tweet_id,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def UnfavoriteTweet(self, tweet_id):
        data = {
            "queryId": "ZYKSe-w7KEslx3JhSIk5LA",
            "variables": json.dumps(
                {
                    "tweet_id": tweet_id,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/ZYKSe-w7KEslx3JhSIk5LA/UnfavoriteTweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def CreateRetweet(self, tweet_id):
        data = {
            "queryId": "ojPdsZsimiJrUGLR1sjUtA",
            "variables": json.dumps(
                {
                    "tweet_id": tweet_id,
                    "dark_request": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def DeleteRetweet(self, tweet_id):
        data = {
            "queryId": "iQtK4dl5hBmXewYZuEOKVw",
            "variables": json.dumps(
                {
                    "source_tweet_id": tweet_id,
                    "dark_request": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/iQtK4dl5hBmXewYZuEOKVw/DeleteRetweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self


    # Legacy API v1.1

    def friendships_create(self, tweet_id):
        data = {
            "include_profile_interstitial_type": 1,
            "include_blocking": 1,
            "include_blocked_by": 1,
            "include_followed_by": 1,
            "include_want_retweets": 1,
            "include_mute_edge": 1,
            "include_can_dm": 1,
            "include_can_media_tag": 1,
            "include_ext_has_nft_avatar": 1,
            "skip_status": 1,
            "id": tweet_id,
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/friendships/create.json",
            headers=self.__get_headers_legacy(),
            data=data,
        ).json()
        self.content = response
        return self

    def friendships_destroy(self, tweet_id):
        data = {
            "include_profile_interstitial_type": 1,
            "include_blocking": 1,
            "include_blocked_by": 1,
            "include_followed_by": 1,
            "include_want_retweets": 1,
            "include_mute_edge": 1,
            "include_can_dm": 1,
            "include_can_media_tag": 1,
            "include_ext_has_nft_avatar": 1,
            "skip_status": 1,
            "id": tweet_id,
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/friendships/destroy.json",
            headers=self.__get_headers_legacy(),
            data=data,
        ).json()
        self.content = response
        return self


    #追加--
    
    def get_dm_inbox(self):
            response = self.session.get('https://twitter.com/i/api/1.1/dm/inbox_initial_state.json', headers=self.__get_headers_legacy(), timeout=30).json()
            self.content = response
            return self

    def get_dm(self, max_id=''):

        if max_id == '':
            response = self.session.get('https://api.twitter.com/1.1/dm/user_inbox.json', headers=self.__get_headers_legacy(), timeout=30).json()

        else:
            data = {
                'max_conv_count': '50',
                'include_groups': 'true',
                'max_id': max_id,
                'cards_platform': 'Web-13',
                'include_entities': '0',
                'include_user_entities': '0',
                'include_cards': '0',
                'send_error_codes': '1',
                'tweet_mode': 'extended',
                'include_ext_alt_text': 'true',
                'include_reply_count': 'true',
            }
            
            response = self.session.get('https://api.twitter.com/1.1/dm/user_inbox.json', headers=self.__get_headers_legacy(), data=data, timeout=30).json()

        self.content = response
        return self

    
    def get_dm_more(self, max_id='999999999999999999999999'):
        
        data = {
            'max_conv_count': '50',
            'include_groups': 'true',
            'max_id': max_id,
            'cards_platform': 'Web-13',
            'include_entities': '0',
            'include_user_entities': '0',
            'include_cards': '0',
            'send_error_codes': '1',
            'tweet_mode': 'extended',
            'include_ext_alt_text': 'true',
            'include_reply_count': 'true',
        }
        
        response = self.session.get('https://api.twitter.com/1.1/dm/user_inbox.json', headers=self.__get_headers_legacy(), data=data, timeout=30).json()
        self.content = response
        return self

    
    def get_conversation(self, conversation_id=''):


        url = 'https://api.twitter.com/1.1/dm/conversation/{}.json'.format(conversation_id)
        # data = {
        #     'ext': 'altText',
        #     'count': '100',
        #     'max_id': max_id,
        #     'cards_platform': 'Web-13',
        #     'include_entities': '1',
        #     'include_user_entities': '1',
        #     'include_cards': '1',
        #     'send_error_codes': '1',
        #     'tweet_mode': 'extended',
        #     'include_ext_alt_text': 'true',
        #     'include_reply_count': 'true',
        # }
        
        response = self.session.get(url, headers=self.__get_headers_legacy(), timeout=30).json()
        self.content = response
        return self

    def send_dm(self, text, screen_name=None, user_id=None):
        if screen_name == None:
            if user_id == None:
                print("Neither 'screen_name' nor 'user_id' was entered.")
            else:
                data = {
                    'recipient_ids': user_id,
                    'text': text
                }

                response = self.session.post('https://twitter.com/i/api/1.1/dm/new.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        else:
            response = self.session.get('https://api.twitter.com/1.1/users/show.json?screen_name=' + screen_name, headers=self.__get_headers_legacy(),timeout=30).json()
            data = {
                'recipient_ids': response['id'],
                'text': text
            }

            response = self.session.post('https://twitter.com/i/api/1.1/dm/new.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        self.content = response
        return self
    

    #アカウント設定用

    def user_info(self, screen_name=None, user_id=None):
        if screen_name == None:
            if user_id == None:
                print("Neither 'screen_name' nor 'user_id' was entered.")
            else:
                response = self.session.get('https://api.twitter.com/1.1/users/show.json?user_id=' + user_id, headers=self.__get_headers_legacy(),timeout=30).json()
        else:
            response = self.session.get('https://api.twitter.com/1.1/users/show.json?screen_name=' + screen_name, headers=self.__get_headers_legacy(),timeout=30).json()

        self.content = response
        return self

    def verify_password(self, password):
        data = {
            'password': password
        }
        
        response = self.session.post('https://twitter.com/i/api/1.1/account/verify_password.json', headers=self.__get_headers_legacy(), data=data)
        # self.content = response.json() | json.dumps(response.cookies.get_dict())
        self.content = response.json()
        return self

    def account_data(self, verify=None, password=""):
        if verify == None:
            data = {
                'password': password
            }

            response = self.session.post('https://twitter.com/i/api/1.1/account/verify_password.json', headers=self.__get_headers_legacy(), data=data)
            if "errors" in response.json():
                print(response.json()["errors"][0]["message"])
            elif response.json()["status"] == "ok":
                # cookie = self.headers["cookie"] + '; _twitter_sess=' + response.cookies.get_dict()["_twitter_sess"]
                # self.headers["cookie"] = cookie

                response = self.session.get('https://twitter.com/i/api/1.1/account/personalization/p13n_data.json', headers=self.__get_headers_legacy(),timeout=30).json()

        elif not verify == None:
            # cookie = self.headers["cookie"] + '; _twitter_sess=' + verify
            # self.headers["cookie"] = cookie

            response = self.session.get('https://twitter.com/i/api/1.1/account/personalization/p13n_data.json', headers=self.__get_headers_legacy(),timeout=30).json()

        self.content = response
        return self

    
    def display_sensitive_media(self, display='true'):

        data = {
            'display_sensitive_media': display.lower()
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self

    def change_country(self, country_code="jp"):
    
        data = {
            "country_code": country_code
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self

    def change_lang(self, lang="ja"):
        
        data = {
            "language": lang
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self
    
    def pin_tweet(self, id):
        data = {
            'id': id
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/pin_tweet.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        return response

    def unpin_tweet(self, id):
        data = {
            'id': id
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/unpin_tweet.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        self.content = response
        return self

    def change_id(self, id):
        data = {
            'screen_name': id
        }
        
        response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        self.content = response
        return self

    def private(self, protected):
        if not protected.lower() in ["true", "false"]:
            print("""Please enter "true" or "false".""")
        elif protected.lower() in ["true", "false"]:
            data = {
                'protected': protected
            }
            
            response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        self.content = response
        return self

    def gender(self, gender='female'):
        if gender.lower() in ["female", "male"]:
            data = '{"preferences":{"gender_preferences":{"use_gender_for_personalization":true,"gender_override":{"type":"' + gender.lower() + '","value":"' + gender.lower() + '"}}}}'

            response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        else:
            data = '{"preferences":{"gender_preferences":{"use_gender_for_personalization":true,"gender_override":{"type":"custom","value":"' + gender.lower() + '"}}}}'

        self.content = response
        return self


    def allow_dm(self, allow_dms_from='all'):
        #allow_dms_from = 'all' or 'following'

        data = {
            'include_mention_filter': 'true',
            'include_nsfw_user_flag': 'true',
            'include_nsfw_admin_flag': 'true',
            'include_ranked_timeline': 'true',
            'include_alt_text_compose': 'true',
            'allow_dms_from': allow_dms_from,
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self

    def dm_filter(self):
        #allow_dms_from = 'all' or 'following'

        data = {
            'include_mention_filter': 'true',
            'include_nsfw_user_flag': 'true',
            'include_nsfw_admin_flag': 'true',
            'include_ranked_timeline': 'true',
            'include_alt_text_compose': 'true',
            'dm_quality_filter': 'disabled',
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self
    
    def update_profile(self, data):
        """
        Args:
            data (dict): 
            {
                'birthdate_year': '2000',
                'birthdate_month': '1',
                'birthdate_day': '1',
                'birthdate_visibility': 'self',
                'birthdate_year_visibility': 'self',
                'displayNameMaxLength': 50,
                'url': 'https://twitter.com/aaa',
                'name': 'bot',
                'description': 'yoyo!',
                'location': 'JP'
            }
        """
        response = self.session.post('https://twitter.com/i/api/1.1/account/update_profile.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self
    
    def update_profile_image(self, img_path):
        src_img = Image.open(img_path).convert('RGB')
        img_str = pil_to_base64(src_img)
        data = {
            'image': img_str
        }
        response = self.session.post('https://twitter.com/i/api/1.1/account/update_profile_image.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self


    def favorites_list(self, screen_name, count=None, since_id=None, max_id=None, include_entities=None, tweet_mode=None):
        url = 'https://api.twitter.com/1.1/favorites/list.json?screen_name=' + screen_name
        if count != None:
            url = url + '&count=' + count
        if since_id != None:
            url = url + '&since_id=' + since_id
        if max_id != None:
            url = url + '&max_id=' + since_id
        if include_entities != None:
            url = url + '&include_entities=' + include_entities
        if tweet_mode != None:
            url = url + '&tweet_mode=' + tweet_mode
        response = self.session.get(url, headers=self.__get_headers_legacy(),timeout=30).json()
        self.content = response
        return self

    def followers_ids(self, screen_name, cursor=None, stringify_ids=None, count=None):
        url = 'https://api.twitter.com/1.1/followers/ids.json?screen_name=' + screen_name
        if cursor != None:
            url = url + '&cursor=' + cursor
        if stringify_ids != None:
            url = url + '&stringify_ids=' + stringify_ids
        if count != None:
            url = url + '&count=' + count
        response = self.session.get(url, headers=self.__get_headers_legacy(),timeout=30).json()
        self.content = response
        return self

    def followers_list(self, screen_name, cursor=None, count=None, skip_status=None, include_user_entities=None, tweet_mode=None):
        url = 'https://api.twitter.com/1.1/followers/list.json?screen_name=' + screen_name
        if cursor != None:
            url = url + '&cursor=' + cursor
        if count != None:
            url = url + '&count=' + count
        if skip_status != None:
            url = url + '&skip_status=' + skip_status
        if include_user_entities != None:
            url = url + '&include_user_entities=' + include_user_entities
        if tweet_mode != None:
            url = url + '&tweet_mode=' + tweet_mode
        response = self.session.get(url, headers=self.__get_headers_legacy(),timeout=30).json()
        self.content = response
        return self

    def friends_ids(self, screen_name, cursor=None, stringify_ids=None, count=None):
        url = 'https://api.twitter.com/1.1/friends/ids.json?screen_name=' + screen_name
        if cursor != None:
            url = url + '&cursor=' + cursor
        if stringify_ids != None:
            url = url + '&stringify_ids=' + stringify_ids
        if count != None:
            url = url + '&count=' + count
        response = self.session.get(url, headers=self.__get_headers_legacy(),timeout=30).json()
        self.content = response
        return self

    def friends_list(self, screen_name, cursor=None, count=None, skip_status=None, include_user_entities=None, tweet_mode=None):
        url = 'https://api.twitter.com/1.1/friends/list.json?screen_name=' + screen_name
        if cursor != None:
            url = url + '&cursor=' + cursor
        if count != None:
            url = url + '&count=' + count
        if skip_status != None:
            url = url + '&skip_status=' + skip_status
        if include_user_entities != None:
            url = url + '&include_user_entities=' + include_user_entities
        if tweet_mode != None:
            url = url + '&tweet_mode=' + tweet_mode
        response = self.session.get(url, headers=self.__get_headers_legacy(),timeout=30).json()
        self.content = response
        return self

    def friendships_show(self, source_screen_name, target_screen_name):
        url = 'https://api.twitter.com/1.1/friendships/show.json?source_screen_name=' + source_screen_name + '&target_screen_name=' + target_screen_name
        response = self.session.get(url, headers=self.__get_headers_legacy(),timeout=30).json()
        self.content = response
        return self

    def friendships_show(self, source_screen_name, target_screen_name):
        url = 'https://api.twitter.com/1.1/friendships/show.json?source_screen_name=' + source_screen_name + '&target_screen_name=' + target_screen_name
        response = self.session.get(url, headers=self.__get_headers_legacy(),timeout=30).json()
        self.content = response
        return self

    def friendships_show_with_id(self, source_id, target_id):
        url = 'https://api.twitter.com/1.1/friendships/show.json?source_id=' + source_id + '&target_id=' + target_id
        response = self.session.get(url, headers=self.__get_headers_legacy(),timeout=30).json()
        self.content = response
        return self
    
    def searchbox(self, text):
        params = (
            ('q', text),
            ('src', 'search_box'),
        )
        response = self.session.get('https://twitter.com/i/api/1.1/search/typeahead.json', headers=self.__get_headers_legacy(), params=params,timeout=30).json()

        self.content = response
        return self

    def topic_search(self, text):
        params = (
            ('q', text),
            ('tweet_search_mode', 'extended'),
        )
        response = self.session.get('https://twitter.com/i/api/2/search/adaptive.json', headers=self.__get_headers_legacy(), params=params,timeout=30).json()

        self.content = response
        return self

    def latest_search(self, text, count=None):
        params = (
            ('q', text),
            ('tweet_search_mode', 'live'),
        )

        url = 'https://twitter.com/i/api/2/search/adaptive.json'
        if count != None:
            url = url + '&count=' + count

            
        response = self.session.get(url, headers=self.__get_headers_legacy(), params=params,timeout=30).json()

        self.content = response
        return self

    def image_search(self, text):
        params = (
            ('q', text),
            ('tweet_mode', 'extended'),
            ('result_filter', 'image'),
        )
        response = self.session.get('https://twitter.com/i/api/2/search/adaptive.json', headers=self.__get_headers_legacy(), params=params,timeout=30).json()

        self.content = response
        return self

    def video_search(self, text):
        params = (
            ('q', text),
            ('tweet_mode', 'extended'),
            ('result_filter', 'video'),
        )
        response = self.session.get('https://twitter.com/i/api/2/search/adaptive.json', headers=self.__get_headers_legacy(), params=params,timeout=30).json()

        self.content = response
        return self

    def shadowban_check(self, screen_name=None):
        if not screen_name == None:
            no_tweet = False
            protect = False

            suspend = False
            not_found = False

            search_ban = False
            search_suggestion_ban = False
            ghost_ban = False
            reply_deboosting = False

            #add
            id_str = ""
            followers_count = 0
            friends_count = 0

            adaptive = requests.get("https://api.twitter.com/2/search/adaptive.json?q=from:" + screen_name + "&count=20&spelling_corrections=0", headers=self.__get_headers_legacy())
            typeahead = requests.get("https://api.twitter.com/1.1/search/typeahead.json?src=search_box&result_type=users&q=" + screen_name, headers=self.__get_headers_legacy())
            show = requests.get("https://api.twitter.com/1.1/users/show.json?screen_name=" + screen_name, headers=self.__get_headers_legacy())

            if "errors" in show.json():
                if show.json()["errors"][0]["code"] == 63:
                    suspend = True
                elif show.json()["errors"][0]["code"] == 50:
                    not_found = True

            else:
                if show.json()["protected"] == False:
                    id_str = show.json()['id_str']
                    followers_count = show.json()['followers_count']
                    friends_count = show.json()['friends_count']
                    
                    if "status" in show.json():
                        profile = requests.get("https://api.twitter.com/2/timeline/profile/" + str(show.json()["id"]) +".json?include_tweet_replies=1&include_want_retweets=0&include_reply_count=1&count=1000", headers=self.__get_headers_legacy())

                        if adaptive.json()['globalObjects']['tweets']:
                            pass
                        else:
                            search_ban = True

                        if typeahead.json()["num_results"] == 0:
                            search_suggestion_ban = True
                            
                        # for i in profile.json()["globalObjects"]["tweets"]:
                        #     for _ in profile.json()["globalObjects"]["tweets"][i]:
                        #         if _ == "in_reply_to_status_id_str":
                        #             conversation = requests.get("https://api.twitter.com/2/timeline/conversation/" + str(profile.json()["globalObjects"]["tweets"][i]["in_reply_to_status_id_str"]) + ".json?include_reply_count=1&send_error_codes=true&count=20", headers=self.__get_headers_legacy())
                        #             if conversation.status_code == 404:
                        #                 ghost_ban = True
                        #                 reply_deboosting = True
                        #             else:
                        #                 deboosting_l = []
                        #                 for i in conversation.json()["globalObjects"]["tweets"]:
                        #                     deboosting_l.append(conversation.json()["globalObjects"]["tweets"][i]["user_id_str"])
                        #                 if str(show.json()["id"]) in deboosting_l:
                        #                     pass
                        #                 else:
                        #                     reply_deboosting = True
                        #             break
                        #     else:
                        #         continue
                        #     break

                    else:
                        no_tweet = True
                else:
                    protect = True
        else:
            print("Neither 'screen_name' nor 'user_id' was entered.")

        return {'id_str': id_str, 'screen_name': screen_name, 'followers_count': followers_count, 'friends_count': friends_count, 'no_tweet':no_tweet, 'protect':protect, 'suspend':suspend, 'not_found':not_found, 'search_ban':search_ban, 'search_suggestion_ban':search_suggestion_ban, 'ghost_ban':ghost_ban, 'reply_deboosting':reply_deboosting}
            
    def user_search(self, text, count=20, cursor=''):


        # params = {
        #         "q": text,
        #         "tweet_mode": "extended",
        #         "result_filter": "user",
        #     }
        # if count:
        #     params['count'] = str(count)
        # if cursor:
        #     params['cursor'] = cursor
        


        if cursor:
            params = (
                ('q', text),
                ('tweet_mode', 'extended'),
                ('result_filter', 'user'),
                ('count', str(count)),
                ('cursor', cursor),
            )
        else:
            params = (
                ('q', text),
                ('tweet_mode', 'extended'),
                ('result_filter', 'user'),
                ('count', str(count)),
            )

        
        url = 'https://twitter.com/i/api/2/search/adaptive.json'

        response = self.session.get(url, headers=self.__get_headers_legacy(), params=params,timeout=30).json()

        self.content = response
        return self
    

    def screenname_available(self, id):
        params = (
            ('username', id),
        )
        response = self.session.get('https://twitter.com/i/api/i/users/username_available.json', headers=self.__get_headers_legacy(), params=params,timeout=30).json()

        self.content = response
        return self




def check_shadowban(screen_name):

    cookies = {
        '_gid': 'GA1.2.1399265878.1674472457',
        '__gads': 'ID=2a257c6972d3a938-22ac9d1064d90085:T=1674472455:RT=1674472455:S=ALNI_Mau0agcOSgtJeQ1C5V3SRzscuwyaQ',
        '__gpi': 'UID=00000bab20f9a241:T=1674472455:RT=1674472455:S=ALNI_MbJX_ruQyt1KNwcWzL7C3EjB153jQ',
        '_ga': 'GA1.2.1728721209.1674472456',
        '_gat_gtag_UA_202220676_1': '1',
        '_ga_4E8SDFWKN5': 'GS1.1.1674474354.2.1.1674474473.0.0.0',
        'FCNEC': '%5B%5B%22AKsRol8i2Me0fF1g6CIatYeLVrph9sskVf_N7lPcfwRf7Lf3MujY9EfU5x62xxKMUUzg22Wk74MZiy1juRpuLv0g9mM4d3QfzaiA_63gsG1MyN1rtpMpyrisdpMqrjqG52q_DiDtF-rdPZ5xrwp9V7ypK4_luVbNcg%3D%3D%22%5D%2Cnull%2C%5B%5D%5D',
    }

    headers = {
        'authority': 'taishin-miyamoto.com',
        'accept': '*/*',
        'accept-language': 'ja',
        # 'cookie': '_gid=GA1.2.1399265878.1674472457; __gads=ID=2a257c6972d3a938-22ac9d1064d90085:T=1674472455:RT=1674472455:S=ALNI_Mau0agcOSgtJeQ1C5V3SRzscuwyaQ; __gpi=UID=00000bab20f9a241:T=1674472455:RT=1674472455:S=ALNI_MbJX_ruQyt1KNwcWzL7C3EjB153jQ; _ga=GA1.2.1728721209.1674472456; _gat_gtag_UA_202220676_1=1; _ga_4E8SDFWKN5=GS1.1.1674474354.2.1.1674474473.0.0.0; FCNEC=%5B%5B%22AKsRol8i2Me0fF1g6CIatYeLVrph9sskVf_N7lPcfwRf7Lf3MujY9EfU5x62xxKMUUzg22Wk74MZiy1juRpuLv0g9mM4d3QfzaiA_63gsG1MyN1rtpMpyrisdpMqrjqG52q_DiDtF-rdPZ5xrwp9V7ypK4_luVbNcg%3D%3D%22%5D%2Cnull%2C%5B%5D%5D',
        'referer': 'https://taishin-miyamoto.com/ShadowBan/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }


    params = {
        'screen_name': screen_name,
    }

    response = requests.get('https://taishin-miyamoto.com/ShadowBan/API/JSON', params=params, cookies=cookies, headers=headers, timeout=30).json()
    # print(response)
    return response