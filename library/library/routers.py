class MyRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'books':
            if 'book_id' in hints:
                book_id = hints['book_id']
                return f'book_db{book_id % 3}'
        elif model._meta.app_label == 'users' or model._meta.app_label == 'favorites':
            if 'user_id' in hints:
                user_id = hints['user_id']
                return f'user_db{user_id % 3}'
        return None

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    def allow_relation(self, obj1, obj2, **hints):

        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'books':
            return db.startswith('book_db')
        elif app_label in ['users', 'favorites']:
            return db.startswith('user_db')
        return True
