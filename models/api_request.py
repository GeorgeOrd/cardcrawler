from fake_useragent import UserAgent


class ApiRequest():
    """
    Multiple api requests
    """

    def get_user_agent(self):
        """
        Create a random user agent to prevent IP ban in requests
        """
        user_agent = UserAgent(
            browsers=['Edge', 'Chrome', 'Firefox', 'Android',
                      'Opera Mobile', 'Firefox Mobile', 'Chrome Mobile'],
            os=['Linux', 'Ubuntu', 'Windows', 'Android'],
        )

        headers = {
            'User-Agent': user_agent.random,
        }

        return headers


