## YAML Properties for Inline Code Documentation

### `comment1`, `comment2`, `comment3`

- `comment1`: The opening comment delimiter for the language (e.g., `/**` for C++ or Swift). 
- `comment2`: The comment prefix that begins each line of documentation. For example, in Dart, the comment prefix is `///`, while in Swift it would be `*` if `comment1` is `/**`.
- `comment3`: The closing comment delimiter for the language (e.g., `*/` for C++ or Swift).

### `summary1` and `summary2`

The summary of the method or function being documented. `summary1` is the opening prefix for the summary, while `summary2` is the closing suffix. These properties are used to enclose the summary text. 

### `tag1` and `tag2`

The prefix and suffix for each documentation tag (e.g., `@param` in Java or `:param:` in Python). 

### `param1`, `param2`, and `param3`

The prefix, suffix, and separator for each parameter in the method or function. For example, in Dart, the prefix is `* [`, the suffix is `] `, and there is no separator. 

### `link1` and `link2`

The prefix and suffix for a link to another part of the documentation or external reference. 

### `ignore`

Any string or keyword that indicates that a particular piece of documentation should be ignored by the parser or generator. This can be useful for excluding internal or experimental functions from the documentation.

### `return1`, `return2`, and `return3`

- `return1`: The prefix that is used on the line immediately preceding the return value of the method or function being documented.
- `return2`: The separator that is used on the same line as the content.
- `return3`: The suffix that is used on the line immediately following the return value of the method or function being documented.

By defining these properties in a YAML file, you can automate the process of documenting your code in a consistent and standardized way, no matter what language you are working with.
