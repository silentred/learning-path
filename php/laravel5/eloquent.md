
## 关于预加载 with()

```php

function paginateRecipes(Material $material, $offset, $limit=10){
    return $material->recipes()->limit($limit)->offset($offset)->with(['recipeInfo' => function($query){
        $query->select(['main_material', 'condiment', 'recipe_id']);
    }])->get();
}

```
这里能够看出，with传入一个数组，key是关系，value是对sql的操作，
这里要注意的是，如果用select去选择部分字段，一定要把foreign key这个字段包含在里面，
因为就是靠这个字段把结果与和recipe的id做关联，没有foreign key的话，取得的recipe->recipeInfo永远为null
