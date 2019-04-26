from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class DatabaseHandler:

    def __init__(self):
        self.engine = None
        self.session = None
        self.logger = None

    def init(
            self,
            engine,
            user,
            name,
            logger,
    ):
        """
        Init the DB connection. Does not create the session.
        Args:
            engine (str): engine used for connection
            user (str): DB Username
            password (str): DB User password
            host (str): DB host
            port (int): DB port
            name (str): DB name
            logger (KibanaLogger): Logger used to print information
        """
        self.logger = logger
        try:

            # In order to handle database reconnection we use the pessimistic
            # approach with the `pool_pre_ping` parameter. The connection is
            # checked (using a constant operation) prior every database query.
            # http://docs.sqlalchemy.org/en/latest/core/pooling.html#pool-disconnects-pessimistic
            self.engine = create_engine(
                '%s://%s/%s' % (
                    engine,
                    user,
                    name
                ),
                pool_recycle=3600,
                pool_pre_ping=True,
            )
            self.logger.info(
                {
                    'db_connected': 'Connected to database %s' % (
                        name,
                    )
                }
            )
        except SQLAlchemyError as e:    # pragma: no cover
            self.logger.error({'db_connection_error': 'Database connection error: %s' % str(e)})
            if self.engine is not None:
                self.engine.dispose()
            self.engine = None
        self.session = None

    def create_session(self):
        """
        Create a new session
        """
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def close_session(self):
        """
        Terminate the current session
        """
        if self.session is not None:
            self.session.close()
        self.session = None

    def release(self):
        """
        Properly destroy this handler
        """
        if self.engine is not None:
            self.engine.dispose()
        self.close_session()

    def create(self, obj):
        """
        Add a new object in the database
        Args:
            obj (Model): Object model to add

        Returns:
            bool: True on success
        """
        self.session.add(obj)
        return self.update()

    def update(self):
        """
        Update changes
        Returns:
            bool: True on success
        """
        try:
            self.session.commit()
        except SQLAlchemyError as e:    # pragma: no cover
            self.session.rollback()
            self.logger.error({'db_error': 'Database error: %s' % str(e)})
            return False
        return True

    def remove(self, obj):
        """
        Remove an object from the database
        Args:
            obj: Object to remove

        Returns:
            bool: True if the object has been successfully removed
        """
        self.session.delete(obj)
        return self.update()

    def get(
            self,
            model,
            condition=None
    ):
        """
        Get all objects matching the condition.
        Args:
            model (Model): Object model class
            condition (dict): Filter to apply

        Returns:
            Query: List of object model
        """
        request = self.session.query(model)
        if condition is not None:
            request = request.filter_by(**condition)
        return request

    def get_one(self, model, condition):
        """
        Return the first object found, matching the conditions
        Args:
            model (Model): Object model class
            condition (dict): Filter to apply

        Returns:
            The first object found, or None
        """
        try:
            return self.get(model, condition).first()
        except OperationalError as e:
            self.logger.error({'db_error': 'Database error: %s' % str(e)})
            raise DatabaseError(str(e))
