import os
import subprocess


class LangTester:
    def __init__(self, b_path, f_names):
        self.prefix = "test_"
        self.suffix = ".py"
        self.files = self.__generate_files(b_path, f_names)
        self.checks = self.__read_files()
        self.__run()

    def __generate_files(self, p, n):
        if type(n) == str:
            n = [n]

        if os.path.isdir(p):
            files = list()
            for f in n:
                file = f"{p}/{self.prefix}{f}{self.suffix}"
                if os.path.isfile(file):
                    files.append(file)

            return files
        else:
            raise NameError("Path given is not a directory")

    def __read_files(self):
        checks = list()
        for file in self.files:
            with open(file) as f:
                test = {
                    "status": "",
                    "stdout": "",
                    "file": file
                }

                lines = f.readlines()
                for l in lines:
                    if '#' in l:
                        if 'status:' in l:
                            l = l.split(":")[1].strip()
                            test["status"] = l

                        if 'stdout:' in l:
                            l = l.split(":")[1].strip()
                            test["stdout"] = l
                checks.append(test)
        return checks

    def __run(self):
        end = "{0}: {1}\n"
        for c in self.checks:
            t = os.path.abspath(c['file'])
            cmd = f'python3 "{t}"'
            error = []
            try:
                output = subprocess.check_output(
                    cmd, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
            except subprocess.CalledProcessError as exc:
                error = [exc.returncode, exc.output]
                print(error[1])

            if c['status'] == "success":
                if len(error) > 0:
                    status = False
                else:
                    status = True
            elif c['status'] == "error":
                if len(error) > 0:
                    status = True
                else:
                    status = False

            if c['stdout'] in output.strip():
                stdout = True
            elif len(error) > 0:
                if c['stdout'] in error[1].strip():
                    stdout = True
                else:
                    stdout = False
            else:
                stdout = False

            if status and stdout:
                status = "success"
            else:
                status = "failure"

            print(end.format(os.path.basename(t), status))
