<html>
<body>
<h2>Shopping List</h2>
<hr/>
<table>
% for item in shopping_list:
  <tr>
    <td>{{item['description']}}</td>
    <td><a href="/update/{{str(item['_id'])}}">update</a></td>
    <td><a href="/delete/{{str(item['_id'])}}">delete</a></td>
  </tr>
% end
</table>
<hr/>
<a href="/add">Add new item</a>
</body>
</html>