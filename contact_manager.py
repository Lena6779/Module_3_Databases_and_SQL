from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional
from sqlalchemy import Boolean, create_engine, String, select

engine = create_engine("sqlite:///contacts.db", echo=False)

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contact"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)  # Needed to add id in case there was a contact name duplicated but two different people!
    first_name: Mapped[str] = mapped_column(String(200), nullable=False)
    last_name: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(500), unique=True)
    phone: Mapped[str] = mapped_column(String(20))
    favorite: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return (
            f"Contact(id={self.id!r}, first_name={self.first_name!r}, "
            f"last_name={self.last_name!r}, email={self.email!r}, "
            f"phone={self.phone!r}, favorite={self.favorite!r})"
        )

Base.metadata.create_all(engine)

# FUNCTIONS
def add_contact(first_name, last_name, email, phone=None):
    """Add a new contact. Returns the newly created contact."""
    with Session(engine) as session:
        contact = Contact(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone
        )
        session.add(contact)
        session.commit() # Completes two actions in order: flushes any pending changes then commits them
        session.refresh(contact)
        return contact 

def list_contacts():
    """Returns all contacts sorted by last name then first"""
    with Session(engine) as session: 
        return session.execute(
        select(Contact).order_by(Contact.last_name, Contact.first_name)
        ).scalars().all()

def find_contact(email):    
    """Find a singe contact by email and returns it or None"""   # Bonus function added 
    with Session(engine) as session:
        return session.execute(
        select(Contact).where(Contact.email == email)
        ).scalar_one_or_none()

def update_phone(email, new_phone):
    """Update phone number for a contact and returns True if found BUT False otherwise"""
    with Session(engine) as session:
        contact = session.execute(
        select(Contact).where(Contact.email == email)
        ).scalar_one_or_none()
        if not contact: 
            return False
        contact.phone = new_phone
        session.commit()
        return True

def toggle_favorite(email):
    """Change a contact's favorite status and returns whatever exists as the opposite status or None"""
    with Session(engine) as session:
        contact = session.execute(
            select(Contact).where(Contact.email == email)
        ).scalar_one_or_none()
        if not contact:
            return None
        contact.favorite = not contact.favorite
        session.commit()
        return contact.favorite

def delete_contact(email):
    """Delete a contact by their email and returns True if deleted otherwise False"""
    with Session(engine) as session:
        contact = session.execute(
            select(Contact).where(Contact.email == email)
        ).scalar_one_or_none()
        if not contact:
            return False
        session.delete(contact)
        session.commit()
        return True

# Testing to see if contacts will print
def print_contacts():
    contacts = list_contacts()
    if not contacts:
        print("  (no contacts)")
        return
    for c in contacts:
        fav = "♥ " if c.favorite else "  "
        phone = c.phone or "-"
        email = c.email or "-"
        print(f"  {fav}{c.first_name} {c.last_name:<15} {email:<30} {phone}")

# Inserting Sample Data and Testing Functions

if __name__ == "__main__":
    print("Adding contacts...")
    # Will just add 5 contacts of a fictional family
    add_contact("Thomas", "Doley", "thomas.doley@gmail.com", "777-521-6666") # Child 1
    add_contact("Amelia", "Doley", "amelia.doley@gmail.com", "777-123-8945") # Child 2
    add_contact("Kate", "Doley", "kate.doley@gmail.com", "777-462-3659")# Child 3
    add_contact("Chris", "Doley", "chris.doley@gmail.com", "777-471-7156") # Mom
    add_contact("Carly", "Doley", "carly.doley@gmail.com","777-859-0034") # Dad
    add_contact("Grandpa Joe", "Doley", "joe.doley@yahoo.com","899-421-8947") # Paternal grandfather

    # List contacts 
    print("All contacts:")
    print_contacts()

    # Update phone
    print("Updating Thomas's phone to 777-521-8910")
    update_phone("thomas.doley@gmail.com","777-521-8910")

    # Toggle favorites
    print("Marking Chris and Carly as favorites.")
    toggle_favorite("chris.doley@gmail.com")
    toggle_favorite("carly.doley@gmail.com")

    # Delete one contact
    print("Deleting Grandpa Joe from contacts") # Family member passed away years ago but was still in contacts so needed to be deleted from contacts now (backstory)
    delete_contact("joe.doley@yahoo.com")

    # Find a specific contact
    # BONUS function 
    print("Looking up kate.doley@gmail.com:")
    c = find_contact("kate.doley@gmail.com")
    print(f"Found: {c.first_name} {c.last_name}, favorite={c.favorite}, phone={c.phone}")

    # List contacts again
    print("Final contacts below:")
    print_contacts()
