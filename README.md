# Mawile Detection

## SetUp

```
[ec2-user@ip-x-x-x-X ~]$ sudo yum -y upgrade
[ec2-user@ip-x-x-x-X ~]$ sudo yum -y install git
[ec2-user@ip-x-x-x-X ~]$ sudo yum -y install git tmux emacs gcc gcc-c++ python-setuptools python-devel 
[ec2-user@ip-x-x-x-X ~]$ sudo git clone https://github.com/yyuu/pyenv.git /usr/bin/.pyenv
[ec2-user@ip-x-x-x-X ~]$ cd /usr/bin/.pyenv
[ec2-user@ip-x-x-x-X ~]$ sudo mkdir shims
[ec2-user@ip-x-x-x-X ~]$ sudo mkdir versions
[ec2-user@ip-x-x-x-X ~]$ sudo chown -R ec2-user:ec2-user /usr/bin/.pyenv
[ec2-user@ip-x-x-x-X ~]$ vi ~/.bashrc

export PYENV_ROOT="/usr/bin/.pyenv"
if [ -d "${PYENV_ROOT}" ]; then
export PATH=${PYENV_ROOT}/bin:$PATH
eval "$(pyenv init -)"
fi

[ec2-user@ip-x-x-x-X ~]$ source ~/.bashrc
[ec2-user@ip-x-x-x-X ~]$ pyenv
pyenv 1.2.6
Usage: pyenv <command> [<args>]

Some useful pyenv commands are:
   commands    List all available pyenv commands
   local       Set or show the local application-specific Python version
   global      Set or show the global Python version
   shell       Set or show the shell-specific Python version
   install     Install a Python version using python-build
   uninstall   Uninstall a specific Python version
   rehash      Rehash pyenv shims (run this after installing executables)
   version     Show the current Python version and its origin
   versions    List all Python versions available to pyenv
   which       Display the full path to an executable
   whence      List all Python versions that contain the given executable

See `pyenv help <command>' for information on a specific command.
For full documentation, see: https://github.com/pyenv/pyenv#readme
[ec2-user@ip-x-x-x-X ~]$ pyenv install --list
[ec2-user@ip-x-x-x-X ~]$ pyenv install anaconda3-5.1.0
[ec2-user@ip-x-x-x-X ~]$ pyenv global anaconda3-5.1.0
[ec2-user@ip-x-x-x-X ~]$ python --version
[ec2-user@ip-x-x-x-X ~]$ conda install -c conda-forge jupyterhub
[ec2-user@ip-x-x-x-X ~]$ cd /home/ec2-user/
[ec2-user@ip-x-x-x-X ~]$ mkdir jupyterhub
[ec2-user@ip-x-x-x-X ~]$ cd jupyterhub/
[ec2-user@ip-x-x-x-X ~]$ jupyterhub --generate-config
Writing default config to: jupyterhub_config.py
[ec2-user@ip-x-x-x-X ~]$  vi jupyterhub_config.py

#c.Spawner.notebook_dir = ''
c.Spawner.notebook_dir = '~/notebook'

[ec2-user@ip-x-x-x-X ~]$ echo jupyterhub -f /etc/jupyterhub/jupyterhub_config.py > jupyterhub.sh
[ec2-user@ip-x-x-x-X ~]$ su -l root ./jupyterhub.sh

[1]+  Done                    sudo echo su -l root jupyterhub.sh
[ec2-user@ip-x-x-x-X ~]$ sudo adduser satonaka
[ec2-user@ip-x-x-x-X ~]$ passwd satonaka
passwd: Only root can specify a user name.
[ec2-user@ip-x-x-x-X ~]$ sudo passwd satonaka
Changing password for user satonaka.
New password: 
BAD PASSWORD: The password fails the dictionary check - it is based on a dictionary word
Retype new password: 
passwd: all authentication tokens updated successfully.
[ec2-user@ip-x-x-x-X ~]$ conda -y install keras
[ec2-user@ip-x-x-x-X ~]$ conda -y install tensorflow
[ec2-user@ip-x-x-x-X ~]$ git clone https://github.com/sacchin/mawile_ssd_keras.git
[ec2-user@ip-x-x-x-X ~]$ cd mawile_ssd_keras/
[ec2-user@ip-x-x-x-X ~]$ git checkout add_training_code
[ec2-user@ip-x-x-x-X ~]$ mv /home/ec2-user/kucheat_anotation.zip /home/ec2-user/mawile_ssd_keras/data
[ec2-user@ip-x-x-x-X ~]$ unzip kucheat_anotation.zip
[ec2-user@ip-x-x-x-X ~]$ rm annotations/ -r
[ec2-user@ip-x-x-x-X ~]$ rm images/ -r
[ec2-user@ip-x-x-x-X ~]$ mv origin/ images/
[ec2-user@ip-x-x-x-X ~]$ mv poke/ annotations/



# Google analytics
* プロパティIDを取得
* スクリプトを生成
* 対象のHTMLにスクリプトをはっつける



## 参考
* https://qiita.com/michimani/items/fc64dcbe721d91579ccb
* https://jp.ubunifu.co/python/jupyterhub-pyenv-anaconda%E7%92%B0%E5%A2%83%E6%A7%8B%E7%AF%89%EF%BC%88aws-ec2%EF%BC%89
* https://haitenaipants.hatenablog.com/entry/2018/06/21/210108
* https://recipe.kc-cloud.jp/archives/11084