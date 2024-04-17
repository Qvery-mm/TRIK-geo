$pi_ip = '192.168.30.30'
$pi_user='pi'
$pi_password='raspberry'
$working_dir='/home/pi/aleks'
$working_dir_windows='C:\Users\aleks\PycharmProjects\TRIK-geo'


plink -ssh $pi_user@$pi_ip -pw $pi_password -m create_dirs_pi.sh
pscp -pw $pi_password simple.py $pi_user@${pi_ip}:${working_dir}
plink -ssh $pi_user@$pi_ip -pw $pi_password -m $working_dir_windows\drone\run_python_pi.sh

rm $working_dir_windows\data\frames\*
pscp -pw $pi_password $pi_user@${pi_ip}:${working_dir}/frames/* $working_dir_windows\data\frames