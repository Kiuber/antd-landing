from echobox.tool import functocli
from echobox.tool import template
from echobox.tool import dockerutil
from echobox.app.devops import DevOpsApp

import os

APP_NAME = 'antd-landing-rn'

image = 'docker.io/kiuber/antd-landing-rn:1.0.0'

container_config = {
    'dev': {
        'container_name': 'antd-landing-rn-dev',
        'ports': [
            '10800:3000',
            '10801:5000',
        ],
        'mode': '-it',
    },
    'prod': {
        'container_name': 'antd-landing-rn-prod',
        'ports': [
            '10810:5000',
        ],
        'mode': '-d',
    },
}


class App(DevOpsApp):

    def __init__(self):
        DevOpsApp.__init__(self, APP_NAME)
        self.landing_app_dir = self.root_dir + '/app'

    def _copy_package_config(self):
        self.shell_run('cp %s %s' % (self.landing_app_dir + '/package.json', self.root_dir + '/docker/package.json'))

    def build_image(self):
        self._copy_package_config()
        cmd = 'docker build -t %s %s' % (image, 'docker')
        self.shell_run(cmd)

    def _link_node_modules(self, node_modules_in_host):
        if os.path.exists(node_modules_in_host):
            self.shell_run('rm ' + node_modules_in_host)
        self.shell_run('ln -sf /opt/node_npm_data/node_modules ' + node_modules_in_host)

    def _start(self, script, env):
        self._link_node_modules(self.landing_app_dir + '/node_modules')

        volumes = {
            self.landing_app_dir: '/opt/src',
        }

        args = dockerutil.base_docker_args(container_name=container_config[env]['container_name'], volumes=volumes, ports=container_config[env]['ports'])

        cmd_args = 'npm run %s --prefix /opt/src' % script
        # cmd_args = 'bash'
        cmd_data = {'image': image, 'args': args, 'cmd_args': cmd_args, 'mode': container_config[env]['mode']}
        cmd = template.render_str(
            'docker run {{ mode }} --privileged=true --restart always {{ args }} {{ image }} {{ cmd_args }}', cmd_data)
        self.shell_run(cmd)

    def _restart(self, script, env):
        self._stop(env)
        self._start(script, env)

    def _stop(self, env):
        self.stop_container(container_config[env]['container_name'], timeout=1)
        self.remove_container(container_config[env]['container_name'], force=True)

    def restart_script(self, script='dev'):
        self._restart(script, 'dev')

    def restart(self, script='serve_build'):
        self._restart(script, 'prod')

    def _send_cmd_to_container(self, cmd, env):
        cmd = "docker exec -i %s sh -c '%s'" % (container_config[env]['container_name'], cmd)
        self.shell_run(cmd)

    def build_dest(self):
        cmd = 'npm run build'
        self._send_cmd_to_container(cmd, 'dev')


if __name__ == '__main__':
    functocli.run_app(App)
