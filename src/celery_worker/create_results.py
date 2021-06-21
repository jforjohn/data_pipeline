from os import mkdir, path
from shutil import copyfile
from celery.utils.log import get_task_logger

celery_log = get_task_logger(__name__)

def create_outputdir(config, task_id):
    data_folder = config.get('data', 'folder')
    output_folder = config.get('data', 'output')
    result_path = path.join(data_folder, output_folder)
    if not path.exists(result_path):
        mkdir(result_path)

    task_path = path.join(result_path, str(task_id))
    if not path.exists(task_path):
        mkdir(task_path)
    return task_path

def save_results(df, config, task_id, transformations):
    celery_log.info('Prepare results')
    task_path = create_outputdir(config, task_id)
    celery_log.info(f'Transformations: {transformations}')
    try:
        # save images
        if transformations:
            from .MLDataset import MLDataset
            tranform_img = MLDataset(df.set_index('id'))
            df['id'].map(
                lambda img_id: tranform_img[img_id].save(path.join(task_path, 
                                                          str(img_id)+'.jpg'))
                )
        else:
            df['url'].map(
                lambda x: copyfile(x, path.join(task_path, x.split("/")[-1]))
                )
        df['url'] = df['id'].map(
            lambda x: path.join(task_path, f'{str(x)}.jpg')
            )
        df.to_csv(path.join(task_path, 'metadata.csv'), sep=',')
        celery_log.info(f'Results ready in {task_path}')
        return 'ok'
    except Exception as e:
        msg = f'Error during saving results: {e}'
        celery_log.error(msg)
        #raise Exception(msg)
        return 'not ok'
