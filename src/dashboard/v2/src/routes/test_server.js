const tag_name_value_pairs={
    development:{
        DevelopedId:0,
        UndevelopedId:1
    },
    washover:{
        VisibleWashoverId:0,
        NoVisibleWashoverId:1
    },
    impact:{
        SwashId:0,
        OverwashId:1,
        InundationId:2,
        CollisionId:3
    },
    terrian:{
        RiverId:'RiverId',
        MarshId:'MarshId',
        SandyCoastlineId:'SandyCoastlineId'
    }
}

console.log(tag_name_value_pairs['development']['DevelopedId'])