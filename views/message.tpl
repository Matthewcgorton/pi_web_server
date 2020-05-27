<html>
  <head>
    <style>

      td {
        font-family: sans-serif;
      }

      th {
        font-family: sans-serif;
        font-weight: bold;
      }

    </style>
  </head>
  <body>
    <table>
      <tr><th>Line:</th><th>Message</th></tr>
      <tr><td>Line 1</td><td>{{lcd['msg'][0]}}</td></tr>
      <tr><td>Line 2</td><td>{{lcd['msg'][1]}}</td></tr>
      <tr><td>Line 3</td><td>{{lcd['msg'][2]}}</td></tr>
      <tr><td>Line 4</td><td>{{lcd['msg'][3]}}</td></tr>
    </table>
  </body>
</html>




{ 'enabled' = {{lcd['backlight']}},
  'msg' = ['{{lcd['msg'][0]}}',
           '{{lcd['msg'][1]}}',
           '{{lcd['msg'][2]}}',
           '{{lcd['msg'][3]}}']
}
