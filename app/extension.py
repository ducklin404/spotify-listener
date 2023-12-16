import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sep = os.sep

def proxies(username, password, endpoint, port):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxies",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
              singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
              },
              bypassList: ["localhost"]
            }
          };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (endpoint, port, username, password)

    extension = 'proxies_extension.zip'

    if not os.path.exists(dir_path + sep + 'proxies_extension'):
        os.mkdir(dir_path + sep + 'proxies_extension')
    with open(dir_path + sep + 'proxies_extension' + sep + 'background.js', 'w') as file:
        file.write(background_js)
        
    with open(dir_path + sep + 'proxies_extension' + sep + 'manifest.json', 'w') as file:
        file.write(manifest_json)

    return dir_path + sep + 'proxies_extension'