import os
import yaml
from html import unescape
from rtmbot.core import Plugin

from plugins.code_runner import CodeRunner
from plugins.utils import init_logger


logger = init_logger(__name__)


def get_lang(line):
    texts = line.split()
    if len(texts) == 1:
        return 'bash'
    return texts[1].lower()


def get_config(lang, langs_dir='./langs'):
    for dir_name in sorted(os.listdir(langs_dir)):
        fname = os.path.join(langs_dir, dir_name, 'config.yml')
        config = yaml.load(open(fname))
        if dir_name == lang:
            return config

        if 'aliases' in config and lang in config['aliases']:
            return config

    return None


def format_result(lang, stdout, stderr, exec_time):
    stdout = stdout
    stderr = stderr

    results = ['']
    results.append('言語: {}'.format(lang))
    results.append('実行時間: {}'.format(exec_time))

    if stdout:
        results.append('標準出力:\n {}'.format(stdout))
    if stderr:
        results.append('標準エラー出力:\n {}'.format(stderr))

    return '\n'.join(results)


class OSCommandInjection(Plugin):
    def __init__(self, *args, **kwargs):
        super(OSCommandInjection, self).__init__(*args, **kwargs)
        self.bot_id = self.slack_client.api_call('auth.test')['user_id']
        self.code_runner = CodeRunner('odanado/os-command-injection')

        logger.info('start!')

    def reply(self, channel, to_user, text):
        self.outputs.append([channel, "<@{}> {}".format(to_user, text)])

    def process_message(self, data):
        if 'text' not in data:
            return

        text = data['text']
        if not text.startswith('<@{}>'.format(self.bot_id)):
            return

        user = data['user']
        channel = data['channel']

        lines = text.split('\n')
        lang = get_lang(lines[0])
        config = get_config(lang)
        if config is None:
            self.reply(channel, user, "プログラミング言語 {}が見つかりません.".format(lang))
            return

        source = unescape('\n'.join(lines[1::]))

        logger.info("{} {} {}".format(user, lang, source))
        stdout, stderr, exec_time = self.code_runner.run(source, **config)
        self.reply(channel, user, format_result(
            lang, stdout, stderr, exec_time))
