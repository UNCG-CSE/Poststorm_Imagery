module.exports.getPageTitle= (route) =>  {
	// options = {
	// 	...options
  // };

  const routePageNames=[
    {
      route:"/",
      name:"Welcome to Image Dashboard"
    },
    {
      route:"/auth/tagImage",
      name:"Storm Tagging Selection"
    },
    {
      route:"/auth/dashboardHome",
      name:"Dashboard Home"
    }
  ];

  const filteredPage=routePageNames.filter(
    function(element){ return (element.route == route) }
  )[0]

  return (filteredPage===undefined ? 'ERROR - No Title Found':filteredPage.name)
  

};