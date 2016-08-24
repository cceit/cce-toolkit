def format_form_field_titles(form, label_dict):
    for field, field_obj in form.fields.items():
        field_obj.label = field_obj.label.title()
        for key, value in label_dict.items():
            if field_obj == form.fields[key]:
                field_obj.label = value
