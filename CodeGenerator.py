import fileinput
import os
import sys
from UserSetiing import DataCollectorPath
from TestCaseBodyCode import Body_code
from pipelineBuilderCode import PipelineBuilderCode
from LibraryImporter import Import
from loggerUtility import logger
from global_variable_initializers.GlobalVariableInitializer import GlobalVariable


def generate_code(gitbranch, file_name, test_case):
    build_pipeline_code = ''
    import_object= Import(file_name)
    import_library=import_object.import_library()

    file_name_path = f'{DataCollectorPath}/stage/configuration/{file_name}'
    try:
        for line in fileinput.FileInput(file_name_path, inplace=1):

            if 'import pytest' in line:
                line = line.rstrip()
                line = line.replace(line, f'{import_library}')
            elif f'{test_case}' in line:
                body_code_object = Body_code(file_name, line)
                code = body_code_object.get_body_code()
                pipeline_builder_object = PipelineBuilderCode(file_name, line)
                build_pipeline = pipeline_builder_object.build_pipeline()
                build_pipeline_code = build_pipeline
                line = line.rstrip()
                line = line.replace(line, f'{code}')
            if line.strip("\n") != "from streamsets.testframework.decorators import stub":
                sys.stdout.write(line)
        with open(file_name_path, 'a+') as f:
            f.write(build_pipeline_code)
        global_object = GlobalVariable(file_name_path, test_case)
        global_object.set_global_variable()
        logger.info("successfully generated code ")
    except Exception as error:
        os.system('git checkout master')
        os.system(f'git branch -D {gitbranch}')
        logger.exception(error)
        logger.info(f'git branch {gitbranch} has been deleted')



