```mermaid
classDiagram 
class BaseViews {
    user_content_type = None
    service : ReactionService
    def get() -> list[UserContent]
    create(obj: UserContent) -> UserContent
    delete(id: ObjectId)
}

class ReviewViews {
    user_content_type: UserContent = Reivew
    service = ReviewService
}
class LikeViews {
    user_content_type: UserContent = Like
    service = LikeService
}
```

```python

class BaseViews {
    user_content_type = None
    service : ReactionService
    
    @router.get('')
    def get() -> list[UserContent]
    
    @router.post('')
    create(obj: UserContent) -> UserContent
    
    @router.delete('{id}')
    delete(id: ObjectId)
}
    
@cbv(router) 
class LikeViews {
    user_content_type: UserContent = Like
    service = LikeService
}
    
app.include_router(
    router, prefix='/api/v1/likes/',
    router, prefix='/api/v1/reivews/',
)
```

