
base_path=$(cd `dirname $0`; pwd)

de_folder=$base_path/priv
en_folder=$base_path/priv_en
echo "de_folder=$de_folder"
echo "en_folder=$en_folder"

echo -n  "en(0) or de(1):"
read  cho
if [[ $cho = 0 ]]; then
python3 do_crypto.py en $de_folder $en_folder
echo "---en done."
elif [[ $cho = 1 ]]; then
rm -rf $de_folder
python3 do_crypto.py de $de_folder $en_folder
echo "---de done."
else
echo "Error: not select"
fi