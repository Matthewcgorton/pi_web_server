<html>
  <head>
    <style>
      h2, form {
        font-family: sans-serif;
        font-weight: normal;
      }
    </style>
  </head>
  <body>
    <h2>Please enter the new values for the LCD</h2>
    <form action="{{form_name}}" method="post">
      <ul>
        <li>Line 1: <input name="line1" type="text" /></li>
        <li>Line 2: <input name="line2" type="text" /></li>
        <li>Line 3: <input name="line3" type="text" /></li>
        <li>Line 4: <input name="line4" type="text" /></li>
        <br />
        <li><input value="Update" type="submit" /></li>
      </ul>
    </form>
  </body>
</head>
