from convert_service import ConvertNumberService


convert_service = ConvertNumberService()
number_to_words = convert_service.to_words(500)
number_to_dollars = convert_service.to_dollars(5632)

# print(number_to_words, number_to_dollars)

