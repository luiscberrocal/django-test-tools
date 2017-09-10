import os
import subprocess
from tempfile import NamedTemporaryFile


class GenericCVS(object):
    @classmethod
    def commit(cls, message):
        f = NamedTemporaryFile('wb', delete=False)
        f.write(message.encode('utf-8'))
        f.close()
        subprocess.check_output(cls._COMMIT_COMMAND + [f.name], env=dict(
            list(os.environ.items()) + [(b'HGENCODING', b'utf-8')]
        ))
        os.unlink(f.name)

    @classmethod
    def is_usable(cls):
        try:
            return subprocess.call(
                cls._TEST_USABLE_COMMAND,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE
            ) == 0
        except OSError as e:
            if e.errno == 2:
                # mercurial is not installed then, ok.
                return False
            raise


class Git(GenericCVS):
    """
    Option	Description of Output
    %H      Commit hash
    %h      Abbreviated commit hash
    %T      Tree hash
    %t      Abbreviated tree hash
    %P      Parent hashes
    %p      Abbreviated parent hashes
    %an     Author name
    %ae     Author email
    %ad     Author date (format respects the --date=option)
    %ar     Author date, relative
    %cn     Committer name
    %ce     Committer email
    %cd     Committer date
    %cr     Committer date, relative
    %s      Subject
    """

    _TEST_USABLE_COMMAND = ["git", "rev-parse", "--git-dir"]
    _COMMIT_COMMAND = ["git", "commit", "-F"]

    def __init__(self):
        self.fields = ['%H', '%an', '%ae', '%ad', '%s']

    @classmethod
    def assert_nondirty(cls):
        lines = [
            line.strip() for line in
            subprocess.check_output(
                ["git", "status", "--porcelain"]).splitlines()
            if not line.strip().startswith(b"??")
        ]

        if lines:
            raise Exception(
                "Git working directory is not clean:\n{}".format(
                    b"\n".join(lines)))

    def report(self):
        # git log --pretty=format:"%h - %an, %ad : %s" --date=iso
        #
        # git log --pretty="%h - %s" --author=gitster --since="2008-10-01"
        # --before="2008-11-01" --no-merges -- t/
        format = '|'.join(self.fields)
        try:
            # git-describe doesn't update the git-index, so we do that
            subprocess.check_output(["git", "update-index", "--refresh"])

            # get info about the latest tag in git
            describe_out = subprocess.check_output([
                "git",
                "log",
                '--date=iso',
                '--pretty=format:"{}"'.format(format)
            ], stderr=subprocess.STDOUT
            ).decode()
        except subprocess.CalledProcessError:
            # logger.warn("Error when running git describe")
            return {}

        return describe_out.split('\n')

    @classmethod
    def latest_tag_info(cls):
        try:
            # git-describe doesn't update the git-index, so we do that
            subprocess.check_output(["git", "update-index", "--refresh"])

            # get info about the latest tag in git
            describe_out = subprocess.check_output([
                "git",
                "describe",
                "--dirty",
                "--tags",
                "--long",
                "--abbrev=40",
                "--match=v*",
            ], stderr=subprocess.STDOUT
            ).decode().split("-")
        except subprocess.CalledProcessError:
            # logger.warn("Error when running git describe")
            return {}

        info = {}

        if describe_out[-1].strip() == "dirty":
            info["dirty"] = True
            describe_out.pop()

        info["commit_sha"] = describe_out.pop().lstrip("g")
        info["distance_to_latest_tag"] = int(describe_out.pop())
        info["current_version"] = "-".join(describe_out).lstrip("v")

        return info

    @classmethod
    def add_path(cls, path):
        subprocess.check_output(["git", "add", "--update", path])

    @classmethod
    def tag(cls, name, message):
        command = ["git", "tag", name]
        if message:
            command += ['--message', message]
        subprocess.check_output(command)
