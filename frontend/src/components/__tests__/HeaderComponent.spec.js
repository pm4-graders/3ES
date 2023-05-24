import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Header from '../HeaderComponent.vue'

describe('Header', () => {
  it('renders the title', () => {
    const title = 'My Title'
    const wrapper = mount(Header, {
      props: {
        title
      }
    })
    expect(wrapper.find('[data-test="title"]').text()).toBe(title)
  })
})
