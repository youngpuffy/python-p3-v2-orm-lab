from __init__ import CURSOR, CONN
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self.year}, '{self.summary}', "
            + f"Employee ID: {self.employee_id}>"
        )
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, year):
        if isinstance(year, int) and year >= 2000:
            self._year =  year
        else:
            raise ValueError("Year must be an integer >= 2000")
        
    @property
    def summary(self):
        return self._summary
    
    @summary.setter
    def summary(self, summary):
        if isinstance(summary, str) and len (summary.strip()) > 0:
            self._summary = summary
        else:
            raise ValueError("Summary must be a non-empty string")
        
    @property
    def employee_id(self):
        return self._employee_id
    
    @employee_id.setter
    def employee_id(self, employee_id):
        if isinstance(employee_id, int) and Employee.find_by_id(employee_id):
            self._employee_id = employee_id
        else: 
            raise ValueError("Employee ID must reference an existing employee")
        
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INTEGER,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employees(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = "DROP TABLE IF EXISTS reviews"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        if self.id is None:
            CURSOR.execute(
                """

                INSERT INTO reviews (year, summary, employee_id)
                VALUES(?, ?, ?)
                """,
                (self.year, self.summary, self.employee_id)
            )
            self.id = CURSOR.lastrowid
            type(self).all[self.id] = self
        else:
            self.update()
        CONN.commit()
        

    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        review = cls(year, summary, employee_id)
        review.save()
        return review
        
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
        # Check the dictionary for  existing instance using the row's primary key
        if not row:
            return None
        review_id =row [0]
        if review_id in cls.all:
            return cls.all[review_id]
        review = cls(row[1], row[2], row[3], id=review_id)
        cls.all[review_id] = review
        return review
        
   

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        CURSOR.execute("SELECT * FROM reviews WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None
        

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        CURSOR.execute(
            """

            UPDATE reviews
            SET year = ?, summary = ?, employee_id = ?
            WHERE id = ?
            """,
             (self.year, self.summary, self.employee_id, self.id)
        )
        CONN.commit()
        

    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        CURSOR.execute("DELETE FROM reviews WHERE id = ?",(self.id,))
        CONN.commit()
        if self.id in type(self).all:
            del type(self).all[self.id]
        self.id = None
        

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        CURSOR.execute("SELECT * FROM reviews")
        rows =  CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]
        

