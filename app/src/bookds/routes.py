from fastapi import APIRouter,status,Depends
from fastapi.exceptions import HTTPException
from typing import List
from app.src.bookds.schemas import Book,BookUpdaeModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.src.db.main import get_session
from src.bookds.service import BookService


book_router = APIRouter()

book_service = BookService()

@book_router.get("/books",response_model=List[Book])

async def get_all_books(session:AsyncSession=Depends(get_session)):
    books = book_service.get_all_books(session)
    return books


@book_router.post("/books",status_code=status.HTTP_201_CREATED)

async def create_book(book_data:Book,session:AsyncSession=Depends(get_session))->dict:
    new_book = await book_service.create_books(book_data,session)
    return new_book


    

@book_router.get("/book/{book_id}",response_model=Book)
async def get_book(book_id:int,session:AsyncSession=Depends(get_session))->dict:
        book =await book_service.get_books(book_id,session)

        if book:
            return book
        else:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="book not found"
                        )

@book_router.put("/book/{book_id}",response_model=Book)
async def update_book(book_id:int,book_update_data:BookUpdaeModel,session:AsyncSession=Depends(get_session))->dict:
    update_book = await book_service.update_books(book_id,session)



    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found")

@book_router.delete("/book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int,session:AsyncSession=Depends(get_session)):

    delete = await  book_service.delete_books(book_id,session)
    if book_to_delete:
        return None
    else:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="book not found")
    
