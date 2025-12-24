import os


def get_files_info(working_directory, directory="."):
    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, directory))

        if os.path.commonpath([absolute_path, target_dir]) != absolute_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        metadata = []
        for item in os.listdir(target_dir):
            path = os.path.join(target_dir, item)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            metadata.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(metadata)

    except Exception as e:
        return f"Error: {e}"
