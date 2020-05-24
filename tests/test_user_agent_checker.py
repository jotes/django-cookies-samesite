import unittest
from django_cookies_samesite.user_agent_checker import UserAgentChecker


class TestUserAgentChecker(unittest.TestCase):

    # On init UserAgentChecker class user agent should be parsed ready.
    def test_user_agent_parser_available(self):
        user_agent_checker = UserAgentChecker(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3334.0 "
            "Safari/537.36")
        self.assertEqual(user_agent_checker.__class__.__name__, "UserAgentChecker")
        self.assertEqual(user_agent_checker.user_agent['family'], 'Chrome')
        self.assertEqual(user_agent_checker.user_agent_os['family'], 'Windows')
        self.assertEqual(user_agent_checker.user_agent_string, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                               'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                               'Chrome/66.0.3334.0 Safari/537.36')

    # Function do_not_send_same_site returns true if user agent is null or blank.
    def test_should_return_false_if_user_agent_is_empty(self):
        user_agent_checker = UserAgentChecker()
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)
        user_agent_checker = UserAgentChecker(None)
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)

    def test_should_return_false_only_for_supported_browsers(self):
        # Should return True for unsupported iOS
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/ "
                                              "604.1.21 (KHTML, like Gecko) Version/ 12.0 Mobile/17A6278a "
                                              "Safari/602.1.26")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, True)

        # Should return True for unsupported MAC OS X 10.14 safari browser
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 ("
                                              "KHTML, like Gecko) Version/12.0 Safari/605.1.15")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, True)

        # Should return False for supported MAC OS X 10.14 non safari browser
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 ("
                                              "KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)

        # Should return False for supported MAC OS X 10.6 safari browser
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-en) "
                                              "AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.3 Safari/533.19.4")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)

        # Should return True for unsupported chrome browser version 51 to 66
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                              "like Gecko) Chrome/66.0.3334.0 Safari/537.36")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, True)

        # Should return False for supported chrome browser version > 66
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                              "like Gecko) Chrome/67.0.3334.0 Safari/537.36")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)

        # Should return False for supported chrome browser version < 51
        user_agent_checker = UserAgentChecker("Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                              "Chrome/50.0.3334.0 Safari/537.36")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)

        # Should return True for unsupported UC browsers under 12.13.2
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) "
                                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 "
                                              "UCBrowser/11.5.1.944 Mobile Safari/537.36")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, True)

        # Should return True for unsupported UC browsers under 12.13.2
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) "
                                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 "
                                              "UCBrowser/12.12.3.944 Mobile Safari/537.36")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, True)

        # Should return True for unsupported UC browsers under 12.13.2
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) "
                                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 "
                                              "UCBrowser/12.13.1.944 Mobile Safari/537.36")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, True)

        # Should return False for supported UC browsers >= 12.13.2
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) "
                                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 "
                                              "UCBrowser/12.13.2.1 Mobile Safari/537.36")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)

        # Should return False for Other Browsers
        user_agent_checker = UserAgentChecker("Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.18")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)

        # Should return False for Other Browsers
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 "
                                              "Firefox/64.0")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)

        # Should return False for Other Browsers
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) "
                                              "like Gecko")
        self.assertEqual(user_agent_checker.do_not_send_same_site_policy, False)

    def test_is_chrome_supported_version(self):
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                              "like Gecko) Chrome/67.0.3334.0 Safari/537.36")
        self.assertEqual(user_agent_checker.is_chrome_supported_version(), True)
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                              "like Gecko) Chrome/66.0.3334.0 Safari/537.36")
        self.assertEqual(user_agent_checker.is_chrome_supported_version(), False)
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                              "like Gecko) Chrome/50.0.3334.0 Safari/537.36")
        self.assertEqual(user_agent_checker.is_chrome_supported_version(), True)
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                                              "like Gecko) Chrome/51.0.3334.0 Safari/537.36")
        self.assertEqual(user_agent_checker.is_chrome_supported_version(), False)
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36(KHTML, like Gecko) "
                                              "Ubuntu Chromium/69.0.3497.8 Chrome/69.0.81 Safari/537.36")
        self.assertEqual(user_agent_checker.is_chrome_supported_version(), True)

    def test_is_uc_browser_in_least_supported_version(self):
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) "
                                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 "
                                              "UCBrowser/13.5.1.944 Mobile Safari/537.36")
        self.assertEqual(user_agent_checker.is_uc_browser_in_least_supported_version(), True)
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) "
                                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 "
                                              "UCBrowser/11.5.1.944 Mobile Safari/537.36")
        self.assertEqual(user_agent_checker.is_uc_browser_in_least_supported_version(), False)
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) "
                                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 "
                                              "UCBrowser/12.13.2.944 Mobile Safari/537.36")
        self.assertEqual(user_agent_checker.is_uc_browser_in_least_supported_version(), True)
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) "
                                              "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 "
                                              "UCBrowser/12.13.1.944 Mobile Safari/537.36")
        self.assertEqual(user_agent_checker.is_uc_browser_in_least_supported_version(), False)

    def test_is_unsupported_ios_version(self):
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/ "
                                              "604.1.21 (KHTML, like Gecko) Version/ 12.0 Mobile/17A6278a "
                                              "Safari/602.1.26")
        self.assertEqual(user_agent_checker.is_supported_ios_version(), False)

    def test_mobile_user_issue_28(self):
        user_agent_checker = UserAgentChecker("edX/2.22.0 CFNetwork/1121.2.2 Darwin/19.3.0")
        self.assertEqual(user_agent_checker.is_supported_ios_version(), True)

    def test_is_unsupported_mac_osx_version(self):
        user_agent_checker = UserAgentChecker("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14) AppleWebKit/605.1.15 ("
                                              "KHTML, like Gecko) Version/12.0 Safari/605.1.15")
        self.assertEqual(user_agent_checker.is_supported_mac_osx_safari(), False)


if __name__ == '__main__':
    unittest.main()
