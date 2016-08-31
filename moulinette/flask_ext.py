from flask import Flask
from flask import request


class ExtFlask(Flask):
    def log_exception(self, exc_info):
        """Pretty formatting for exception logging."""
        self.logger.error(
            """
Request:    {method} {path}
JSON Data:  {data}
IP:         {ip}
Agent:      {agent_platform} | {agent_browser} {agent_browser_version}
Raw Agent:  {agent}
            """.format(
                method=request.method,
                path=request.path,
                data=request.get_json(),
                ip=request.remote_addr,
                agent_platform=request.user_agent.platform,
                agent_browser=request.user_agent.browser,
                agent_browser_version=request.user_agent.version,
                agent=request.user_agent.string,
            ), exc_info=exc_info
        )
