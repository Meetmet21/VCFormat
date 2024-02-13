# DESCRIPTION
# Class to write the changes made with the reader object on a vcf file.

# MODULES

# VARIABLES

# CLASS
class Writer:

    def __init__(self, vcf_output_path, Reader):
        # Output file path
        self.output = vcf_output_path
        # Reader object from which retrieve data
        self.reader = Reader

    def _write_header(self) -> str:
        """
        Concatenate all header names to form the header section from
        Reader object.
        :return: String
        """
        return "\t".join(self.reader.header)

    def _write_metadata(self) -> str:
        """
        Concatenate information for each metadatasection from Reader object.
        :return: String
        """
        # Resulting metastring
        res = ""
        # Fpr each section of metadata
        for meta_name in self.reader.metadata.keys():
            # Write only non-empty metadata fields
            if self.reader.metadata[meta_name]:
                # Join each element of the list corresponding to a record of a section (Ex: INFO)
                res += "\n".join(self.reader.metadata[meta_name]) + "\n"

        return res

    def _write_records(self) -> str:
        """
        Concatenate all records in Reader object.
        :return: String
        """
        # Resulting metastring
        res = ""
        # For each line in all records
        for line in self.reader.records:
            # Concatenate values of dict -> correspond directly to the header configuration
            res += "\t".join(line.values()) + "\n"

        return res

    def update(self):
        """
        Update the output file with the current changes (overwrite) or write the current content of Reader object
        if no changes have been made.
        :return: vcf file
        """
        # Get metadata
        metadata = self._write_metadata()
        # Get header
        header = self._write_header()
        # Get records
        records = self._write_records()
        # Write to output each section in an appropriate order
        with open(self.output, 'w') as file:
            file.write(metadata)
            file.write(header)
            file.write(records)
