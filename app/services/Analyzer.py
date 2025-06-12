import matplotlib.pyplot as plt
from io import BytesIO
import Testing_quality_code as t


def create_diagram(folder_path) :
   dict_image ={}
   data = t.analyze_code(folder_path)
   dict_image["histogram"] = create_lengths_list(data)
   dict_image["pie"] = create_issue_dict(data)
   dict_image["bar"] = create_list_sum_issue(data)


def create_lengths_list(data):
   all_lengths = list(find_key_in_dict(data,"func_length"))
   return create_histogram(all_lengths)


def create_issue_dict(data):
    dict_issue = {
        "Long Functions": sum(1 for i in find_key_in_dict(data, "func_length") if i > 20),
        "Large Files": sum(1 for i in find_key_in_dict(data, "len") if i > 120),
        "Missing Docstrings": sum(1 for i in find_key_in_dict(data, "is_docstring") if not i),
        "Undefined Variables": sum(len(i) for i in find_key_in_dict(data, "list_undefined")),
    }
    return create_issue_pie(dict_issue)


def create_list_sum_issue(data):
    file_data_values = {}
    for filename, file_data in data.items():
        total_issues = find_sum_issue(file_data)
        file_data_values[filename] = total_issues
    return create_bar_sum_issue_for_file(file_data_values)


def find_sum_issue(dict_file):
    sum_all = 0
    sum_all+= sum(1 for i in find_key_in_dict(dict_file, "len") if i > 120)
    sum_all+=sum(1 for i in find_key_in_dict(dict_file, "func_length") if i > 20)
    sum_all+=sum(1 for i in find_key_in_dict(dict_file, "is_docstring") if not i)
    sum_all+=sum(len(i) for i in find_key_in_dict(dict_file, "list_undefined"))
    return sum_all


def create_histogram(lengths):
    plt.figure(figsize=(8, 5))
    plt.hist(lengths, bins=10, color='skyblue', edgecolor='black')
    plt.title("Function Length Distribution")
    plt.xlabel("Function Length (lines)")
    plt.ylabel("Number of Functions")
    plt.grid(True)
    plt.tight_layout()
    plt.gca().yaxis.get_major_locator().set_params(integer=True)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def create_issue_pie(dict_issue):
    labels = list(dict_issue.keys())
    sizes = list(dict_issue.values())
    plt.figure(figsize=(7, 7))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
    colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
    plt.title('Number of Issues by Type')
    plt.axis('equal')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def find_key_in_dict(d, target_key):
    if isinstance(d, dict):
        for key, value in d.items():
            if key == target_key:
                yield value
            else:
                yield from find_key_in_dict(value, target_key)
    elif isinstance(d, list):
        for item in d:
            yield from find_key_in_dict(item, target_key)


def create_bar_sum_issue_for_file(data):
    files = list(data.keys())
    issues = list(data.values())
    plt.figure(figsize=(10, 6))
    plt.bar(files, issues, color='skyblue')
    plt.title('number of problems per file')
    plt.xlabel('file name')
    plt.ylabel('Several problems')
    plt.xticks(rotation=45)
    plt.tight_layout()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

create_diagram(r"C:\Users\user1\Desktop\python\witProjet\classes")




