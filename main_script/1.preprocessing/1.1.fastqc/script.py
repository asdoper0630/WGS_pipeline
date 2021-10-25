# -+- coding: utf-8 -*-

### README START ###
# 이 파일은 fastqc.sh와 같은 폴더에 있어야 합니다.
# fastqc에서 오류가 나타날 경우 이 파일이 아니라 fastqc.sh를 고쳐주세요.
# fastqc.sh에서 사용된 custom parameter는 다음과 같습니다.
# %DIR% : 작업 디렉토리 입력 변수
# %FILES% : 대상 fastq 파일 입력 변수
### README START ###

import os
import glob
import subprocess
import time

# 1. validity test

def valid_dir_fq(dir_str):
    validity = False
    if not os.path.isdir(dir_str): print("submitted directory doesn't exist.")
    else:
        fa,fagz,fq,fqgz = glob.glob('*.fastq'),glob.glob('*.fastq.gz'),glob.glob('*.fq'),glob.glob('*.fq.gz')
        fq_list = fa+fagz+fq+fqgz
        if not fq_list:
            print("your directory doesn't have any raw/compressed fastq files.")
        else:
            if fa:
                filetype = 'fastq'
            elif fagz:
                filetype = 'fastq.gz'
            elif fq:
                filetype = 'fq'
            elif fqgz:
                filetype = 'fq.gz'
            validity = True
    return validity, fq_list, filetype

# 2. target samples

def target_sample(fq_list):
    print('you have following samples.')
    for file in fq_list:
        print(file)
    while True:
        YN = input('Perform QC toward all samples?(Y,N)')
        if YN.lower in ('y','yes'):
            files = set(fq_list)
            break
        elif YN.lower in ('n','no'):
            input_filelist = input('type your samples separated with comma(,).').split(',')
            files = = set(fq_list).intersection(set(input_filelist))
            for target_file in files:
                file = glob.glob(target_file)
                if not file:
                    print(f"input file {target_file} not exist.")
        else:
            print('ERROR : WRONG INPUT.')
    return files

# 3. script individualization

def script_preset(dir,files):
    with open('fastqc.sh') as f:
        script = f.read()
    dirsplit    = script.split('%DIR%')
    filesplit   = ' '.join(dirsplit[0],dir,dirsplit[1]).split('%FILES%')
    processed_script = ' '.join(filesplit[0],' '.join(files),filesplit[1])
    return processed_script

# 4. run fastqc

def run_fastqc(script)
    subprocess.call(script,shell=True)
    with open('fastqc_log.sh','w') as sv:
        sv.write(time.strftime(f"# performed at %Y-%m-%d.%H:%M:%S")+'\n'+script))
    return result

def main():
    validity = False

    # 1. validity test

    while validity == False:
        work_dir = input('input your working directory : ')
        validity, fq_list, filetype = valid_dir_fq()
        if validity == False:
            continue

    # 2. target samples

    files = target_sample(fq_list)

    # 3. script individualization

    if validity == True:
        print(f"you have {str(filecount)} {filetype} sample(s).")
    script = script_preset(work_dir,files)

    # 4. run fastqc
    run_fastqc(script)

main()
