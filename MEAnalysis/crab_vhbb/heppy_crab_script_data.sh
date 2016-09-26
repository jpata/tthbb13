source env.sh
#manually copy the data configuration
cp heppy_config_data.py heppy_config.py
python heppy_crab_script.py $@ &> log
./post.sh $?
