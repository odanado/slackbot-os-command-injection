from constant import Command
from code_runner import code_runner
from client import slack_client as sc
from utils import init_logger

crontable = []
outputs = []

bot_id = sc.api_call('auth.test')['user_id']
logger = init_logger(__name__)


def get_lang(line):
    texts = line.split()
    if len(texts) == 1:
        return 'bash'
    return texts[1].lower()


def reply(channel, to_user, text):
    outputs.append([channel, "<@{}> {}".format(to_user, text)])


def format_result(lang, stdout, stderr, exec_time):
    stdout = stdout.decode('utf8')
    stderr = stderr.decode('utf8')

    results = ['']
    results.append('言語: {}'.format(lang))
    results.append('実行時間: {}'.format(exec_time))

    if stdout:
        results.append('標準出力:\n {}'.format(stdout))
    if stderr:
        results.append('標準エラー出力:\n {}'.format(stderr))

    return '\n'.join(results)


def process_message(data):
    if 'text' not in data:
        return

    text = data['text']
    user = data['user']
    channel = data['channel']

    if text.startswith('<@{}>'.format(bot_id)):
        lines = text.split('\n')
        lang = get_lang(lines[0])
        if lang not in Command:
            reply(channel, user, "プログラミング言語 {}が見つかりません.".format(lang))
            return

        source = '\n'.join(lines[1::])

        logger.info("{} {} {}".format(user, lang, source))
        stdout, stderr, exec_time = code_runner(lang, source)
        reply(channel, user, format_result(lang, stdout, stderr, exec_time))
