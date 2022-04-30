db.createUser({
    user: 'fapi_user',
    pwd: 'fapi_pass',
    roles: [
      {
        role: 'readWrite',
        db: 'db_fapi',
      },
    ],
  });