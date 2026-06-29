def sqlite_casefold(value: str | None) -> str:
    if value is None:
        return ""

    return str(value).casefold()


def register_sqlite_functions(dbapi_connection, _connection_record) -> None:
    run_async = getattr(dbapi_connection, "run_async", None)

    if run_async is not None:
        run_async(
            lambda connection: connection.create_function(
                "casefold",
                1,
                sqlite_casefold,
            )
        )
        return

    dbapi_connection.create_function("casefold", 1, sqlite_casefold)
