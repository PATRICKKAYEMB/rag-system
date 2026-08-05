
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateModel,BookUpdaeModel
from sqlmodel import select,desc
from .model import Book
from datetime import datetime






class BookService:
    async def get_all_books(self,session:AsyncSession):
            statement = select(Book).order_by(desc(Book.create_at))
            retult = await session.exec(statement)


            return retult.all()
    
        

    async def get_books(self,book_uid:str,session:AsyncSession):
            statement = select(Book).where(Book.uid==book_uid)

            result = await session.exec(statement)

            book= result.first()


            return book if book is not None:
    

    async def create_books(self,book_data:BookCreateModel,session:AsyncSession):

                book_data_dict=book_data.model_dump()
                new_book =Book(
                        "book_data_dic"
                )
                new_book.pushisher = datetime.strftime(book_data_dict["published_date"],"y-m-d")
                session.add(new_book)

                await session.commit()

                return new_book

    async def update_books(self,book_uid:str,update_date:BookUpdaeModel,session:AsyncSession):
                book_update = await self.get_books(book_uid,session)

                if book_update is not None:

                    update_data_dict = book_update.model_dump()
                    for k,v in update_data_dict.items():
                            setattr(book_update,k,v)
                    await session.commit()
                    return book_update

                    


    async def delete_books(self,book_uid:str,session:AsyncSession):

                    book_to_delete = await self.get_books(book_uid,session)

                    if book_to_delete is not None:

                            await session.delete(book_to_delete)
                            await session.commit()

                    else:
                            return None
                            
    
