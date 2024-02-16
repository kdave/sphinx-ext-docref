# sphinx-ext-docref

Sphinx `:doc:` + `:ref:` = `:docref:`

## The itch

Sphinx/RST does not(?) have native support for cross references to labels in
specific documents (`:doc:`, `:ref:` but not both at the same time), also
allowing duplicate labels.

If you project uses e.g. html and manual page backends they could share portions
of some text so this would be included from the same source file.  If such file
defines a label then it's not possible to reference the html document, the link
would go to the included document.

Next, the duplicate label is reported, it's not wise to suppress or ignore
warnings.

## The scratch

Implement new role that does the `:doc:` and `:ref:` in one go. A new directive
`duplabel` is used to define a label that is expected to be duplicate (but
otherwise it's an ordinary label) and this gets rid of the warning too.

The label definition in `intro-chapter.rst`:

```rst
.. duplabel:: intro
```

The intro can be included in several documents:

```rst
.. include:: intro-chapter.rst
```

Reference in one document to the label but landing in `Some-doc`:

```rst
:docref:`The intro <Some-doc:intro>`
```

Same but different:

```rst
:docref:`Read more <Another-doc:intgro>`
```

## Misc

The `intersphinx_mapping` does not solve the same problem. It does not work
locally as it expects the file `objects.inv` before build starts (two passes
could possibly fix that). It produces a fixed link for the target, so it cannot
be flexible for html and manual pages.

## Todo

- [x] make it work (html, manual pages), copy & paste to your `conf.py`
- [x] validate target document name
- [ ] validate target label name
- [ ] ref text not mandatory
- [ ] make it a standalone extension
- [ ] add more backends/builders
