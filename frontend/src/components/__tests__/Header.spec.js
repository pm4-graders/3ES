import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Header from '../Header.vue'

describe('Header', () => {
  it('renders the title', () => {
    const title = 'My Title'
    const wrapper = mount(Header, {
      props: {
        title
      }
    })
    expect(wrapper.find('h3').text()).toBe(title)
  })
})
