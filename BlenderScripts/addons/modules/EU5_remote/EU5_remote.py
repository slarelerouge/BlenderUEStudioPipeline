# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


# Does not seem to work on Linux
import sys
from copy import copy
import os
import importlib
#
import config.config as config

# Add path to import remote_execution from
sys.path.append(config.UNREAL_REMOTE_CONTROL_MODULE_DIRECTORY)
import remote_execution as remote
remote.DEFAULT_RECEIVE_BUFFER_SIZE = config.REMOTE_DEFAULT_RECEIVE_BUFFER_SIZE


def reload_remote():
    importlib.reload(remote)
    remote.DEFAULT_RECEIVE_BUFFER_SIZE = config.REMOTE_DEFAULT_RECEIVE_BUFFER_SIZE
    

def needs_unreal(func):
    """
    Decorator to execute the function only if Unreal is running. Else raise an error.

    Args:
        func (function): Function to decorate.
    """
    def _inner(*args, **kwargs):
        connected = 0
        try:
            #reload_remote()
            _create_connection()
            connected = 1
        except:
            connected = 0
            reload_remote()
            raise RuntimeError("Cant connect to unreal. Check that Unreal is running.")

        if connected == 1:
            #print(args, kwargs)
            result = func(*args, **kwargs)
            _close_connection()
            return result

    return _inner


def _create_connection():
    """
    Create a connection with Unreal

    Args:

    """
    global remote_exec
    if remote_exec.has_command_connection() is False:
        remote_exec.start()
        remote_exec.open_command_connection(remote_exec.remote_nodes)
        append_module_to_sys()


def _close_connection():
    """
    Closes the connection with Unreal

    Args:

    """
    global remote_exec
    remote_exec.stop()


@needs_unreal
def execute_python_script(python_script_path, log_to_console=False):
    """
    Run a specific python script in Unreal remotely

    Args:
        python_script_path (string): Path of the python script to execute.
        log_to_console (bool): Whether to log the script filepath and the execution result in the console.
    """

    if log_to_console is True:
        print(python_script_path)

    exec_mode = 'ExecuteFile'
    rec = remote_exec.run_command(python_script_path, exec_mode=exec_mode)

    # Due to the way dictionaries work (they do not copy when assigning it to another dict var),
    # make a real copy of the variable to return it. Just in case _close_connection() modifies it.
    ret = copy(rec)

    if log_to_console is True:
        print(ret)

    return ret


@needs_unreal
def execute_python_command(command, log_to_console=False):
    """
    Run a specific python script in Unreal remotely

    Args:
        command (string): Python string command to run.
        log_to_console (bool): Whether to log the command statement and the execution result in the console.
    """

    exec_mode = 'ExecuteStatement'

    if log_to_console is True:
        print(command)
        remote_exec.run_command(f"print('{command}')", exec_mode=exec_mode)

    rec = remote_exec.run_command(command, exec_mode=exec_mode)

    # Due to the way dictionaries work (they do not copy when assigning it to another dict var),
    # make a real copy of the variable to return it. Just in case _close_connection() modifies it.
    ret = copy(rec)

    return ret


@needs_unreal
def execute_python_function(module, function, *args, log_to_console=False, **kwargs):
    """
    Execute a specific python function

    Args:
        package (string): Python package the function is called from
        module (string): Python module to call the function from
        function (string): Python function to call
    """

    exec_mode = 'ExecuteStatement'

    # Tuple args to proper args in case there is only one arg
    if len(args) == 1:
        args = f'"{args[0]}"'
    else:
        args = str(args)[1:-1]

    # kwargs to function input
    _kwargs = ""
    if len(kwargs) != 0:
        _kwargs = ", "
        for k in kwargs:
            _kwargs += k + "="
            content = kwargs[k]
            if isinstance(content, str):
                _kwargs += '"' + content + '", '
            else:
                _kwargs += str(content) + ', '
    
    command = f'__import__("importlib").import_module("{module}").{function}({args}{_kwargs})'
    
    if log_to_console is True:
        print(command)
        remote_exec.run_command(f"print('{command}')", exec_mode=exec_mode)
    
    ret = remote_exec.run_command(command, exec_mode=exec_mode)

    return ret


def append_module_to_sys():
    exec_mode = 'ExecuteStatement'

    current_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    unreal_script_directory = os.path.join(current_directory, "UnrealScript")
    config_directory = os.path.join(current_directory, "config")
    
    command_import_sys = "import sys"
    remote_exec.run_command(command_import_sys, exec_mode=exec_mode)
    command_set_syspath = f'sys.path.append(r"{current_directory}")'
    remote_exec.run_command(command_set_syspath, exec_mode=exec_mode)


# CORE
remote_exec = remote.RemoteExecution()
