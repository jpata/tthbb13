source env.sh
python heppy_crab_script.py $@ &> log
./post.sh $?
