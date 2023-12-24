import os
import zipfile

dir_path = os.path.dirname(os.path.realpath(__file__))
sep = os.sep


def proxies(username, password, endpoint, port):
    manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 3,
    "name": "Chrome Proxy Authentication",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "webRequest",
        "webRequestAuthProvider"
    ],
    "host_permissions": [
        "<all_urls>"
    ],
    "background": {
        "service_worker": "background.js"
    },
    "minimum_chrome_version": "108"
}
"""

    background_js = """
var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: %s
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
    { urls: ["<all_urls>"] },
    ['blocking']
);
""" % (
        endpoint,
        port,
        username,
        password,
    )

    print()
    extension = 'proxies_extension.zip'

    if not os.path.exists(dir_path + sep + 'proxies_extensionssssssss'):
        os.mkdir(dir_path + sep + 'proxies_extensionssssssss')
    with open(dir_path + sep + 'proxies_extensionssssssss' + sep + 'background.js', 'w') as file:
        file.write(background_js)

    with open(dir_path + sep + 'proxies_extensionssssssss' + sep + 'manifest.json', 'w') as file:
        file.write(manifest_json)

    # with zipfile.ZipFile(dir_path + sep + extension, 'w') as zp:
    #     zp.writestr("manifest.json", manifest_json)
    #     zp.writestr("background.js", background_js)

    return dir_path + sep + 'proxies_extensionssssssss'
