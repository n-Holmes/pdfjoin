from pdfrw import PdfReader, PdfWriter, IndirectPdfDict, PdfName


def concatenate(input_paths, output_path, details):
    """Given an ordered sequence of paths to pdf files, concatenate
    to the desired output path with the given details.
    
    Args:
        input_paths: A sequence of paths to pdf files.
        output_path: The desired path for the concatenated pdf.
        details: A dictionary of metadata values desired for the final pdf.
    """
    writer = PdfWriter()

    for path in input_paths:
        reader = PdfReader(path)
        writer.addpages(reader.pages)

    writer.trailer.Info = IndirectPdfDict()
    for metadata, value in details.items():
        writer.trailer.Info[PdfName(metadata)] = value

    writer.write(output_path)
